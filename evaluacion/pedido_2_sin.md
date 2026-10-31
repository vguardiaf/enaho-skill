# pedido_2_sin

Pedido: Grafica la pobreza urbana y rural

Skills: []

Costo: 0.84 USD

Hice el gráfico de pobreza urbana y rural con la ENAHO 2024: la pobreza rural (39,3 %) supera a la urbana (24,8 %) por unos 14,5 puntos. Incluí la barra nacional como referencia, y los intervalos de confianza no se traslapan, así que la diferencia es estadísticamente clara.

| Área | Pobreza total (IC 95 %) | Pobreza extrema | Pobreza no extrema | Personas pobres |
|---|---|---|---|---|
| Urbana | **24,8 %** (23,6–26,0) | 3,1 % | 21,7 % | 6,9 millones |
| Rural | **39,3 %** (37,7–41,0) | 15,5 % | 23,8 % | 2,6 millones |
| Nacional | **27,6 %** (26,6–28,6) | 5,5 % | 22,1 % | 9,5 millones |

- **Pobreza extrema:** es donde más se separan las dos áreas: la rural es unas cinco veces la urbana.
- **Número de personas:** aunque la tasa rural es mayor, cerca de 7 de cada 10 personas pobres viven en zonas urbanas.

**Decisiones de cálculo**
- **Datos y unidad:** usé `sumaria-2024.dta`, y `sumaria-2024-12g.dta` da los mismos resultados. La pobreza se mide en personas (`factor07 × mieperho`), no en hogares.
- **Urbano y rural:** urbano son los estratos 1 a 5, y rural los estratos 6 a 8. El estrato 6 (500 a 1 999 habitantes) va como rural porque la Ficha Técnica lo ubica en el marco muestral rural. Si fuera urbano, la tasa rural subiría a 41,3 % y la urbana a 24,9 %.
- **Intervalos de confianza:** son una aproximación, porque usan `conglome` y `estrato` como diseño muestral, sin la estratificación por departamento. Podrían diferir un poco de los que publica el INEI.

**Sin verificar:** no pude comparar las cifras con la publicación del INEI, porque la búsqueda web no tenía permiso en esta sesión. El 27,6 % nacional coincide con la cifra oficial que recuerdo, pero conviene contrastar las cifras urbana y rural antes de citarlas.

Los archivos están en la carpeta del proyecto; el script se vuelve a correr con `uv run python pobreza_urbana_rural.py`:
- `resultados/pobreza_urbana_rural_2024.png`
- `resultados/pobreza_urbana_rural_2024.csv`
- `pobreza_urbana_rural.py`
