# Creación de Dashboard en Power BI a partir de una API

Este proyecto consiste en la construcción de un dashboard en Power BI a partir
de datos obtenidos desde una API externa.

Los datos son extraídos mediante la librería **Requests** en Python, consumiendo
la API y transformando la respuesta en estructuras tabulares. Posteriormente, se
utiliza **Pandas** para limpiar, estructurar y organizar la información en un
**modelo estrella**, compuesto por tablas de dimensiones y una tabla de hechos.

Una vez generado el modelo de datos, las tablas son cargadas en una base de datos
**Oracle 21c** utilizando la librería **oracledb** de Python. Sobre Oracle, se
realizan procesos adicionales de transformación y validación de datos mediante
**SQL Developer**, asegurando la integridad y consistencia de la información.

Posteriormente, los datos transformados son transferidos a un **Data Warehouse
en Snowflake** utilizando la librería
**snowflake.connector.pandas_tools** desde Python.

Finalmente, una vez los datos se encuentran en Snowflake, se establece la
conexión desde **Power BI**, donde se construye el dashboard para el análisis
visual de la información.

## Arquitectura del proyecto

El flujo de datos del proyecto sigue el siguiente proceso:
![Pipeline de datos](Imagenes/ELT.png)


