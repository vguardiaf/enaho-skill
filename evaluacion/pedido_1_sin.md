# pedido_1_sin

Pedido: ¿Cuál fue la pobreza en Cusco en 2024?

Skills: []

Costo: 0.54 USD

**En 2024, el 18,5 % de la población de Cusco era pobre**, unas 261 mil de sus 1,41 millones de personas. La pobreza extrema fue de 2,1 %. Son cifras que calculé con la ENAHO 2024 (`sumaria-2024.dta`), no el dato publicado por el INEI.

| Indicador | Cusco | IC 95 % | CV | Nacional |
|---|---|---|---|---|
| Pobreza total | **18,5 %** | 14,6 – 22,4 | 10,7 % | 27,6 % |
| Pobreza extrema | **2,1 %** | 0,9 – 3,3 | 28,4 % | 5,5 % |

**Cómo lo calculé:** usé pobreza monetaria (`pobreza` 1 y 2 para el total, 1 para la extrema) y filtré Cusco con el `ubigeo` que empieza en `08`. Ponderé por personas (`factor07 × mieperho`). Los errores estándar consideran el diseño muestral, con conglomerados dentro de estratos. La muestra de Cusco es de 1.230 hogares y 3.862 personas.

**Precisión:**
- **Pobreza total:** es una estimación aceptable, pero su intervalo es amplio, de unos ±4 puntos. Conviene no sobreinterpretar diferencias pequeñas frente a otros años o departamentos.
- **Pobreza extrema:** es poco precisa (CV de 28 %), así que tómala como un orden de magnitud.

**Verificaciones:**
- **Nacional:** da 27,58 % y 5,50 %, que coincide con lo que recuerdo del INEI (27,6 % y 5,5 %).
- **Versiones de Sumaria:** `sumaria-2024.dta` y `sumaria-2024-12g.dta` dan resultados idénticos.
- **Clasificación de pobreza:** al comparar el gasto con la línea de pobreza coincide en el 99,9 % de los hogares.
- **Tamaño de hogar:** `mieperho` coincide en todos los hogares con el conteo del Módulo 200.

**Sin verificar:** no pude comparar el dato de Cusco con la publicación del INEI porque no tengo permiso para buscar en la web. El INEI suele presentar los departamentos en grupos de pobreza, así que quizá no publique un valor puntual comparable.

También quedó una carpeta `.venv` en el directorio de trabajo, creada por `uv`; los datos originales no cambiaron.
