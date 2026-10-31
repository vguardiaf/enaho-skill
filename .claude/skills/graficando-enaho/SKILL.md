---
name: graficando-enaho
description: Grafica la pobreza monetaria del Perú con la ENAHO del INEI en barras ponderadas por área urbana o rural, sexo o grupos de edad, y guarda el PNG en figuras/. Úsala cuando pidan un gráfico, una figura o barras de la pobreza, o graficar la pobreza urbana y rural, por sexo o por edad.
argument-hint: "[area|sexo|edad]"
allowed-tools: Bash(uv run *), Read
---
# Graficar la ENAHO

Trabaja desde la raíz del repositorio.

1. Si no existe salidas/personas_2024.parquet, usa primero la skill limpiando-enaho.
2. Elige el corte según el pedido: area, sexo o edad. Si te lo pasan como argumento, usa $ARGUMENTS.
3. Corre exactamente: uv run "${CLAUDE_SKILL_DIR}/scripts/graficar.py" --por <corte>
4. Responde con las cifras que imprime el script y la ruta de la figura.

El script fija las reglas de diseño: pondera con facpob07, barras desde cero y ordenadas, un solo color, el valor escrito, título con qué y cuándo, nota de fuente y PNG a 200 dpi en figuras/. No grafiques por otra vía.

Si piden un corte que el script no tiene, avísalo y agrégalo a scripts/graficar.py manteniendo esas reglas.