# Motor-de-Scraping

Este repositorio contiene un pipeline ETL (Extracción, Transformación y Carga) ligero implementado en Python. El objetivo del proyecto es automatizar la ingesta y limpieza de datos no estructurados (HTML) hacia formatos tabulares y estructurados, aplicando buenas prácticas de desarrollo.

Para evitar problemas de bloqueos, el scraper consume datos de [Books to Scrape](http://books.toscrape.com/), un sandbox de prueba estandarizado.

## Arquitectura del Script

El código está estructurado en tres fases desacopladas para mantener la separación de responsabilidades (Separation of Concerns):

1. **Extract (`fetch_html`):** 
   - Realiza peticiones HTTP controladas.
   - Implementa manejo de excepciones (bloques `try/except`) y `timeouts` estrictos para evitar bloqueos de hilo por latencia de red.
2. **Transform (`parse_products` & `generate_summary`):**
   - Transforma el árbol DOM en estructuras de diccionarios de Python.
   - Realiza sanitización de texto y *type casting* defensivo (ej. conversión del string `"£17.46"` a un primitivo `float` para habilitar operaciones aritméticas).
   - Calcula métricas agregadas en memoria.
3. **Load (I/O local):**
   - Persiste los datos transformados en dos formatos: `.csv` (óptimo para análisis tabular/pandas) y `.json` (óptimo para consumo web/APIs).

## Ejecución Local

1. Clonar el repositorio:
```bash
git clone [https://github.com/tu-usuario/ecommerce-scraper-etl.git](https://github.com/tu-usuario/ecommerce-scraper-etl.git)
cd ecommerce-scraper-etl
