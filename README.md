# Skills para limpiar, graficar y mapear la ENAHO

Proyecto de la sesión 16 del curso de Ciencia de Datos con Python. Tres skills de Claude Code convierten los módulos 34 y 02 de la ENAHO 2024 del INEI en una base de personas, gráficos y un mapa de pobreza, siempre de la misma forma.

| Skill | Entra | Sale |
|---|---|---|
| `limpiando-enaho` | Zip de los módulos 34 y 02 | `salidas/personas_2024.parquet`, `salidas/validacion.txt` |
| `graficando-enaho` | La base limpia y un corte: área, sexo o edad | `figuras/*.png` |
| `mapeando-enaho` | La base limpia y los límites departamentales | `mapas/pobreza_departamento.png` |

Si falta la base limpia, las skills de gráficos y mapas usan primero `limpiando-enaho`.

## Resultados

| Cifra | Resultado | Referencia |
|---|---|---|
| Pobreza nacional, personas con `facpob07` | 27.53 % | 27.6 % |
| Pobreza nacional, sumaria con `factor07 × mieperho` | 27.58 % | 27.6 % |
| Pobreza extrema | 5.50 % | 5.5 % |
| Residentes habituales | 108,664 | 108,664 |
| Departamentos con dato | 25 | 25 |

La comparación con y sin skills está en [evaluacion.md](evaluacion.md).

## Requisitos

- [uv](https://docs.astral.sh/uv/)
- [Claude Code](https://code.claude.com/docs)

## Instalación

```bash
git clone https://github.com/vguardiaf/enaho-skill.git
cd enaho-skill
uv sync
mkdir -p datos
```

## Datos

La carpeta `datos/` no se sube. Baja estos tres archivos ahí, sin descomprimir:

```bash
curl -L -o datos/966-Modulo34.zip https://proyectos.inei.gob.pe/iinei/srienaho/descarga/STATA/966-Modulo34.zip
curl -L -o datos/966-Modulo02.zip https://proyectos.inei.gob.pe/iinei/srienaho/descarga/STATA/966-Modulo02.zip
curl -L -o datos/peru_departamental_simple.geojson https://raw.githubusercontent.com/d2cml-ai/Data-Science-Python/main/sessions/06-geoespacial/lab/Data/peru_departamental_simple.geojson
```

## Uso

Abre Claude Code en la raíz del repositorio y pide, por ejemplo:

- ¿Cuál fue la pobreza en Cusco en 2024?
- Grafica la pobreza urbana y rural
- Haz un mapa de la pobreza por departamento

También puedes correr los scripts sin Claude:

```bash
uv run .claude/skills/limpiando-enaho/scripts/limpiar.py --anio 2024
uv run .claude/skills/graficando-enaho/scripts/graficar.py --por area
uv run .claude/skills/mapeando-enaho/scripts/mapear.py
```

## Método

- La base contiene a los residentes habituales, según la definición del INEI.
- Las llaves y el `ubigeo` se conservan como texto para no perder ceros a la izquierda.
- La unión personas-hogares usa `validate="m:1"`, y el mapa une `ubigeo[:2]` con `FIRST_IDDP`.
- Las cifras de la base se ponderan con `facpob07`, por lo que pueden diferir hasta 0.51 puntos por departamento de las referencias de la clase, calculadas con `factor07 × mieperho`.
- Solo 2024 está validado.

## Evaluación

```bash
uv run evaluar.py
```

El script corre seis pedidos con `claude -p`, consume cuota y borra `salidas/`, `figuras/` y `mapas/` antes de cada pedido con skills.