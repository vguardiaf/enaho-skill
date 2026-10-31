"""Grafica la pobreza monetaria de la ENAHO por área, sexo o edad.

Decisiones de método:
- Toda tasa se pondera con facpob07: es la suma de los factores de los pobres entre la
  suma de los factores del grupo.
- Los grupos de edad son 0 a 17, 18 a 29, 30 a 59 y 60 o más.
- El diseño está fijo aquí para que cada figura salga igual: barras desde cero y
  ordenadas, un solo color, el valor escrito, título con qué y cuándo, fuente y 200 dpi.
"""
import argparse
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

BASE = Path(__file__).resolve().parents[4]
SALIDAS = BASE / "salidas"
FIGURAS = BASE / "figuras"

COLOR = "#1f5a8c"
TITULOS = {"area": "área", "sexo": "sexo", "edad": "grupo de edad"}
BORDES_EDAD = [-1, 17, 29, 59, 200]
ETIQUETAS_EDAD = ["0 a 17 años", "18 a 29 años", "30 a 59 años", "60 años o más"]


def agrupar(base, por):
    if por == "area":
        return base["urbano"].map({True: "Urbana", False: "Rural"})
    if por == "sexo":
        return base["p207"].map({1: "Hombres", 2: "Mujeres"})
    return pd.cut(base["p208a"], bins=BORDES_EDAD, labels=ETIQUETAS_EDAD).astype("object")


def pobreza_por_grupo(base, por):
    grupo = agrupar(base, por)
    assert grupo.notna().all(), f"hay personas sin grupo en {por}"
    peso = base["facpob07"].astype("float64")
    tabla = pd.DataFrame({"grupo": grupo, "peso": peso, "peso_pobre": peso * base["pobre"]})
    sumas = tabla.groupby("grupo")[["peso", "peso_pobre"]].sum()
    return (100 * sumas["peso_pobre"] / sumas["peso"]).sort_values()


def graficar(pobreza, por, anio, ruta):
    fig, ax = plt.subplots(figsize=(8, 4.5))
    barras = ax.barh(pobreza.index, pobreza.values, color=COLOR)
    ax.bar_label(barras, fmt="%.1f %%", padding=4)
    ax.set_xlim(0, pobreza.max() * 1.15)
    ax.set_xlabel("% de personas")
    ax.set_title(f"Pobreza monetaria por {TITULOS[por]}, Perú {anio}", loc="left", fontweight="bold")
    ax.spines[["top", "right"]].set_visible(False)
    fig.text(0.01, 0.01, f"Fuente: INEI, ENAHO {anio}", fontsize=9)
    fig.tight_layout(rect=(0, 0.05, 1, 1))
    fig.savefig(ruta, dpi=200)
    plt.close(fig)


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--por", required=True, choices=sorted(TITULOS))
    parser.add_argument("--anio", type=int, default=2024)
    args = parser.parse_args()

    entrada = SALIDAS / f"personas_{args.anio}.parquet"
    if not entrada.exists():
        sys.exit(f"Falta {entrada.name}. Usa primero la skill limpiando-enaho.")

    base = pd.read_parquet(entrada)
    pobreza = pobreza_por_grupo(base, args.por)

    FIGURAS.mkdir(exist_ok=True)
    ruta = FIGURAS / f"pobreza_{args.por}.png"
    graficar(pobreza, args.por, args.anio, ruta)

    for grupo, valor in pobreza.sort_values(ascending=False).items():
        print(f"{grupo}: {valor:.1f} %")
    print(f"Guardado {ruta.relative_to(BASE)}")


if __name__ == "__main__":
    main()