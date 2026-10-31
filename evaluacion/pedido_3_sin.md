# pedido_3_sin

Pedido: Haz un mapa de la pobreza por departamento

Skills: []

Costo: 0.87 USD

El mapa de pobreza monetaria por departamento (ENAHO 2024) está listo, junto con un panel que ordena los departamentos con sus intervalos de confianza. La tasa nacional sale 27,6% (pobreza extrema 5,5%), igual a la cifra oficial de INEI que recuerdo; no la contrasté con la publicación. Las departamentales no tienen esa referencia, porque INEI suele publicarlas por grupos y no una a una.

- **Mayor pobreza:** Cajamarca (45,0%), Loreto (43,0%), Puno (39,9%), Pasco (39,0%) y Huánuco (39,0%).
- **Menor pobreza:** Ica (6,0%), Moquegua (11,0%), Madre de Dios (11,1%) y Lambayeque (14,0%).
- **Lima:** 27,1%, casi igual al promedio nacional, y concentra un tercio de la población.
- **Callao:** 33,9%, muy por encima de Lima. Es tan pequeño que solo se ve con una línea guía.

**Método:**
- Usé la variable oficial `pobreza` de Sumaria, y `factor07 × mieperho` como ponderador para que las tasas sean de personas, no de hogares.
- Los intervalos de confianza consideran el diseño muestral (conglomerado y estrato).
- `sumaria-2024.dta` y la versión `-12g` son idénticas en las variables usadas, así que el resultado no cambia. El Módulo 02 no hizo falta.

**Cautelas al leer el mapa:**
- **Ranking:** no es exacto, porque los intervalos tienen unos ±4 a 5 puntos en la mayoría de departamentos. Cajamarca y Loreto, por ejemplo, no se distinguen estadísticamente, y Cajamarca cae en la clase más alta por estar justo en el corte de 45%.
- **Precisión baja:** Ica, Moquegua y Madre de Dios tienen un coeficiente de variación mayor a 15%; van marcados con `*`.
- **Lima:** incluye Lima Metropolitana y Lima Provincias juntas, así que esconde diferencias internas.
- **Bordes:** son los del GeoJSON simplificado, así que algunos se ven rectos o con pequeños huecos. No afecta a las cifras.

Dejé en la carpeta las extracciones (`extraido/`) y dos scripts de exploración (`scripts/explorar.py` e `inspeccionar.py`). El mapa no los necesita, porque `mapa_pobreza.py` lee directamente de los zip y se regenera con `uv run python -I scripts/mapa_pobreza.py`.

Archivos en `salida/`:
- `mapa_pobreza_departamento_2024.png`
- `pobreza_departamento_2024.csv`
