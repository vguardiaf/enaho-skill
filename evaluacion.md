# Evaluación: tres pedidos con y sin skills

Los pedidos se corrieron con `evaluar.py`, una vez cada uno. Con skills, cada pedido partió sin salidas. Sin skills, cada pedido corrió en una copia temporal fuera del repositorio. Las respuestas completas están en `evaluacion/` y las figuras sin skills en `evaluacion/sin_skills/`.

| Pedido | Modo | Skills activadas | Cifra | Ponderador | Salida | Costo estimado (USD) |
|---|---|---|---|---|---|---|
| ¿Cuál fue la pobreza en Cusco en 2024? | Con | `limpiando-enaho` | 18.54 % | `facpob07` | Texto | 0.40 |
| | Sin | Ninguna | 18.5 % | `factor07 × mieperho` | Texto, con intervalo de confianza | 0.54 |
| Grafica la pobreza urbana y rural | Con | `graficando-enaho`, `limpiando-enaho` | 24.7 % y 39.4 % | `facpob07` | `figuras/pobreza_area.png` | 0.38 |
| | Sin | Ninguna | 24.8 % y 39.3 % | `factor07 × mieperho` | `resultados/`, con barra nacional e intervalos | 0.84 |
| Haz un mapa de la pobreza por departamento | Con | `mapeando-enaho`, `limpiando-enaho` | Cajamarca 45.0 %, Ica 5.9 % | `facpob07` | `mapas/pobreza_departamento.png` | 0.36 |
| | Sin | Ninguna | Cajamarca 45.0 %, Ica 6.0 % | `factor07 × mieperho` | `salida/`, con clases y panel de intervalos | 0.87 |

El costo es la estimación que reporta `claude -p`.

## Hallazgos

- **Activación:** las skills se activaron solas en los tres pedidos, aunque ninguno menciona la ENAHO. Los pedidos 2 y 3 activaron dos skills seguidas.
- **Exactitud:** sin skills, las cifras también fueron correctas. Claude ponderó, unió por código y replicó la pobreza nacional.
- **Qué aportan las skills:** con ellas, el método, las rutas y el diseño son siempre los mismos, y el costo total fue 1.14 USD frente a 2.25 USD.
- **Qué se pierde:** sin skills, Claude agregó intervalos de confianza por iniciativa propia. Las skills no los calculan.
- **Ponderador:** con `facpob07`, las cifras difieren hasta 0.51 puntos de las de la clase, que usan `factor07 × mieperho`. Por eso `mapear.py` valida las referencias con el método de la clase.

## Limitaciones

- Es una sola corrida por pedido, así que los costos son indicativos.
- La evaluación usó `--setting-sources project`, sin skills ni hooks personales.
- El primer intento del pedido 3 con skills se detuvo porque Claude usó PowerShell sin permiso. Se corrigió con `.claude/settings.json`; la tabla muestra la corrida posterior.