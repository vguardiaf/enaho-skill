# pedido_3_con

Pedido: Haz un mapa de la pobreza por departamento

Skills: ['mapeando-enaho', 'limpiando-enaho']

Costo: 0.36 USD

El mapa de pobreza por departamento (ENAHO 2024) ya está en `mapas/pobreza_departamento.png`, con los 25 departamentos con dato. Como faltaba la base de personas, primero corrí la limpieza. Esa validación dio `RESULTADO: OK`, y el chequeo del mapa contra las referencias departamentales también pasó.

| | Departamento | Pobreza (% de personas) |
|---|---|---|
| **Mayor** | Cajamarca | 45.0 |
| | Loreto | 42.6 |
| | Puno | 40.4 |
| **Menor** | Ica | 5.9 |
| | Moquegua | 10.9 |
| | Madre de Dios | 11.1 |

- **Diferencia con las referencias:** las cifras van ponderadas con `facpob07`, y las referencias usan `factor07 x mieperho`. Por eso Puno da 40.4 frente a 39.9 y Loreto 42.6 frente a 43.0; esa diferencia es esperada, no un error.
- **Lima y Callao:** van separados, con 26.9 % y 33.8 %. El polígono de Callao es tan pequeño que casi no se ve en el mapa.

También se regeneraron `salidas/validacion.txt` y `salidas/personas_2024.parquet`. No hice ningún commit.
