"""Limpia los módulos 34 (sumaria) y 02 (miembros) de la ENAHO y arma una base de personas.

Decisiones de método:
- Se lee sumaria-2024.dta por su nombre exacto: el zip trae también sumaria-2024-12g.dta
  y las cifras de referencia salen de la primera.
- Se leen códigos, no etiquetas (convert_categoricals=False), y las llaves quedan como
  texto para conservar los ceros a la izquierda.
- Residentes habituales, según el INEI: miembros que no se ausentaron 30 días o más y
  no miembros que estuvieron presentes 30 días o más.
- ubigeo, dominio y estrato se toman solo de la sumaria, para que la unión no cree
  columnas repetidas con sufijos _x y _y.
- La pobreza se valida de dos formas: sumaria con factor07 x mieperho y personas con
  facpob07. Ambas deben quedar a 0.1 puntos de la cifra oficial.
- El parquet solo se guarda si pasan todas las validaciones.
"""
import argparse
import io
import re
import sys
import zipfile
from pathlib import Path

import pandas as pd

BASE = Path(__file__).resolve().parents[4]
DATOS = BASE / "datos"
SALIDAS = BASE / "salidas"

CODIGOS = {2024: 966}  # código de cada año en el portal de microdatos del INEI
OFICIAL = {
    2024: {
        "hogares": 33691,
        "filas_miembros": 117721,
        "residentes": 108664,
        "pobreza": 27.6,
        "extrema": 5.5,
    }
}

LLAVES = ["conglome", "vivienda", "hogar"]
LLAVES_PERSONA = LLAVES + ["codperso"]
COLUMNAS_HOGAR = LLAVES + ["ubigeo", "dominio", "estrato", "pobreza", "mieperho", "factor07"]
COLUMNAS_PERSONA = LLAVES_PERSONA + ["anio", "p203", "p204", "p205", "p206", "p207", "p208a", "facpob07"]


def normalizar(columna):
    columna = columna.lower()
    return "anio" if re.fullmatch(r"a.{1,2}o", columna) else columna


def leer_dta(ruta_zip, nombre):
    if not ruta_zip.exists():
        sys.exit(f"Falta {ruta_zip.name} en datos/. Bájalo del portal de microdatos del INEI.")
    with zipfile.ZipFile(ruta_zip) as z:
        candidatos = [n for n in z.namelist() if n.endswith("/" + nombre)]
        if len(candidatos) != 1:
            sys.exit(f"No encontré {nombre} en {ruta_zip.name}.")
        crudo = z.read(candidatos[0])
    df = pd.read_stata(io.BytesIO(crudo), convert_categoricals=False)
    df.columns = [normalizar(c) for c in df.columns]
    return df


def como_texto(df, columnas):
    for columna in columnas:
        df[columna] = df[columna].astype(str).str.strip()
    return df


def tasa(df, indicador, peso):
    pesos = df[peso].astype("float64")
    return 100 * (pesos * indicador).sum() / pesos.sum()


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--anio", type=int, default=2024, choices=sorted(CODIGOS))
    anio = parser.parse_args().anio
    codigo = CODIGOS[anio]
    oficial = OFICIAL[anio]

    SALIDAS.mkdir(exist_ok=True)
    salida = SALIDAS / f"personas_{anio}.parquet"
    salida.unlink(missing_ok=True)

    # 1 y 2. Leer y normalizar
    sumaria = leer_dta(DATOS / f"{codigo}-Modulo34.zip", f"sumaria-{anio}.dta")
    miembros = leer_dta(DATOS / f"{codigo}-Modulo02.zip", f"enaho01-{anio}-200.dta")
    filas_miembros = len(miembros)

    sumaria = como_texto(sumaria[COLUMNAS_HOGAR].copy(), LLAVES + ["ubigeo"])
    miembros = como_texto(miembros[COLUMNAS_PERSONA].copy(), LLAVES_PERSONA)
    assert sumaria["ubigeo"].str.len().eq(6).all(), "ubigeo perdió ceros a la izquierda"
    assert sumaria["conglome"].str.len().eq(6).all(), "conglome perdió ceros a la izquierda"

    # 3. Filtrar residentes habituales
    residente = ((miembros["p204"] == 1) & (miembros["p205"] == 2)) | (
        (miembros["p204"] == 2) & (miembros["p206"] == 1)
    )
    personas = miembros.loc[residente].copy()
    assert not personas.duplicated(LLAVES_PERSONA).any(), "personas repetidas"

    # 4. Unir personas y hogares
    base = personas.merge(sumaria, on=LLAVES, how="left", validate="m:1", indicator=True)
    assert len(base) == len(personas), "la unión duplicó filas"
    assert (base["_merge"] == "both").all(), "hay personas sin hogar en la sumaria"
    base = base.drop(columns="_merge")
    assert base[["pobreza", "facpob07"]].notna().all().all(), "hay pobreza o factor vacíos"
    assert base["pobreza"].isin([1, 2, 3]).all(), "pobreza tiene códigos inesperados"

    # 5. Construir variables
    base["departamento"] = base["ubigeo"].str[:2]
    base["urbano"] = base["estrato"] <= 5
    base["pobre"] = base["pobreza"] <= 2
    base["extremo"] = base["pobreza"] == 1

    # 6. Validar
    sumaria["peso"] = sumaria["factor07"].astype("float64") * sumaria["mieperho"]
    chequeos = [
        ("hogares en la sumaria", len(sumaria), oficial["hogares"], 0),
        ("filas del modulo 02", filas_miembros, oficial["filas_miembros"], 0),
        ("residentes habituales", len(base), oficial["residentes"], 0),
        ("pobreza, sumaria con factor07 x mieperho", tasa(sumaria, sumaria["pobreza"] <= 2, "peso"), oficial["pobreza"], 0.1),
        ("pobreza, personas con facpob07", tasa(base, base["pobre"], "facpob07"), oficial["pobreza"], 0.1),
        ("pobreza extrema, sumaria con factor07 x mieperho", tasa(sumaria, sumaria["pobreza"] == 1, "peso"), oficial["extrema"], 0.1),
    ]

    lineas = [f"Validacion ENAHO {anio}", ""]
    fallas = []
    for nombre, valor, esperado, tolerancia in chequeos:
        correcto = abs(valor - esperado) <= tolerancia
        lineas.append(f"{'OK   ' if correcto else 'FALLA'} {nombre}: {valor:,.2f} (esperado {esperado:,}, tolerancia {tolerancia})")
        if not correcto:
            fallas.append(nombre)

    urbano, rural = base[base["urbano"]], base[~base["urbano"]]
    lima = base[base["dominio"] == 8]
    cusco = base[base["departamento"] == "08"]
    lineas += [
        "",
        "Informativo, personas con facpob07:",
        f"extrema: {tasa(base, base['extremo'], 'facpob07'):.2f} %",
        f"urbano: {tasa(urbano, urbano['pobre'], 'facpob07'):.2f} %",
        f"rural: {tasa(rural, rural['pobre'], 'facpob07'):.2f} %",
        f"Lima Metropolitana: {tasa(lima, lima['pobre'], 'facpob07'):.2f} %",
        f"Cusco: {tasa(cusco, cusco['pobre'], 'facpob07'):.2f} %",
        "",
        "RESULTADO: " + ("OK" if not fallas else "FALLA"),
    ]
    texto = "\n".join(lineas)
    (SALIDAS / "validacion.txt").write_text(texto + "\n", encoding="utf-8")
    print(texto)
    assert not fallas, f"Validación fallida: {fallas}"

    # 7. Guardar
    base.to_parquet(salida, index=False)
    print(f"Guardado {salida.relative_to(BASE)}: {len(base):,} personas")


if __name__ == "__main__":
    main()