"""Corre los tres pedidos de la clase con y sin skills y guarda lo que hizo Claude.

Decisiones de método:
- Solo se cargan los ajustes del proyecto, para que skills y hooks personales no
  compitan con las del repositorio.
- Con skills se borran las salidas antes de cada pedido: si la base limpia ya existiera,
  no se probaría el encadenamiento.
- Sin skills se trabaja en una copia temporal fuera del repositorio, sin .claude/ ni el
  mapa de referencia, para que Claude no pueda leer los scripts ni copiar el resultado.
"""
import argparse
import json
import os
import shutil
import subprocess
import tempfile
from pathlib import Path

BASE = Path(__file__).resolve().parent
EVALUACION = BASE / "evaluacion"
LOGS = EVALUACION / "logs"

PEDIDOS = {
    1: "¿Cuál fue la pobreza en Cusco en 2024?",
    2: "Grafica la pobreza urbana y rural",
    3: "Haz un mapa de la pobreza por departamento",
}
HERRAMIENTAS = ["Skill", "Read", "Write", "Edit", "Bash", "PowerShell"]
LIMITE_SEGUNDOS = 900


def borrar_salidas():
    for ruta in [BASE / "salidas" / "personas_2024.parquet", BASE / "salidas" / "validacion.txt"]:
        ruta.unlink(missing_ok=True)
    for carpeta in ["figuras", "mapas"]:
        for ruta in (BASE / carpeta).glob("*.png"):
            ruta.unlink()


def copia_limpia():
    carpeta = Path(tempfile.mkdtemp(prefix="enaho_sin_skills_"))
    shutil.copytree(BASE / "datos", carpeta / "datos")
    (carpeta / "datos" / "mapa_pobreza_2024.png").unlink(missing_ok=True)
    for archivo in ["pyproject.toml", "uv.lock"]:
        shutil.copy(BASE / archivo, carpeta / archivo)
    return carpeta


def guardar_figuras(carpeta, destino):
    for ruta in carpeta.rglob("*.png"):
        if ".venv" in ruta.parts:
            continue
        destino.mkdir(parents=True, exist_ok=True)
        shutil.copy(ruta, destino / ruta.name)


def correr(pedido, carpeta, sin_skills, log):
    comando = ["claude", "-p", pedido, "--setting-sources", "project"]
    comando += ["--output-format", "stream-json", "--verbose", "--allowedTools", *HERRAMIENTAS]
    if sin_skills:
        comando += ["--disallowedTools", "Skill"]
    entorno = {**os.environ, "ECC_GATEGUARD": "off"}
    entorno.pop("VIRTUAL_ENV", None)
    with log.open("wb") as salida:
        subprocess.run(
            comando, cwd=carpeta, env=entorno, stdout=salida,
            stderr=subprocess.STDOUT, timeout=LIMITE_SEGUNDOS,
        )


def leer(log):
    skills, respuesta, costo = [], "(sin respuesta, revisa el log)", 0
    for linea in log.read_text(encoding="utf-8", errors="replace").splitlines():
        try:
            evento = json.loads(linea)
        except json.JSONDecodeError:
            continue
        if evento.get("type") == "assistant":
            for parte in evento["message"]["content"]:
                if parte.get("type") == "tool_use" and parte.get("name") == "Skill":
                    skills.append(parte["input"].get("skill", ""))
        elif evento.get("type") == "result":
            respuesta = evento.get("result") or respuesta
            costo = evento.get("total_cost_usd", 0)
    return skills, respuesta, costo


def evaluar(numero, modo):
    pedido = PEDIDOS[numero]
    nombre = f"pedido_{numero}_{modo}"
    print(f"--- {nombre}: {pedido}", flush=True)
    log = LOGS / f"{nombre}.jsonl"
    if modo == "con":
        borrar_salidas()
        correr(pedido, BASE, False, log)
    else:
        carpeta = copia_limpia()
        correr(pedido, carpeta, True, log)
        guardar_figuras(carpeta, EVALUACION / "sin_skills" / f"pedido_{numero}")
        shutil.rmtree(carpeta, ignore_errors=True)

    skills, respuesta, costo = leer(log)
    texto = f"# {nombre}\n\nPedido: {pedido}\n\nSkills: {skills}\n\nCosto: {costo:.2f} USD\n\n{respuesta}\n"
    (EVALUACION / f"{nombre}.md").write_text(texto, encoding="utf-8")
    print(texto, flush=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--pedido", type=int, nargs="+", default=sorted(PEDIDOS), choices=sorted(PEDIDOS))
    parser.add_argument("--modo", nargs="+", default=["con", "sin"], choices=["con", "sin"])
    args = parser.parse_args()

    LOGS.mkdir(parents=True, exist_ok=True)
    for modo in args.modo:
        for numero in args.pedido:
            evaluar(numero, modo)


if __name__ == "__main__":
    main()