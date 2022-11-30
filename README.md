# Maven_pizza_2016

Maven_pizza pero con datos erróneos.
Haremos un filtrado de los datos antes de realizar el mismo proceso que en maven_pizza

Para ello, hemos de ejecutar el archivo predictions.py
Al ejecutarlo, generará un .csv, un .xml y un reporte formatos .pdf y .xlsx
Los archivos resultantes de predictions estarán alojados en la carpeta conclusiones,
las imágenes empleadas en la carpeta imágenes, y si se ha debido manipular algún .csv,
este se guardará en la carpeta existente datasets

De forma adicional se han creado dos ramas on distintos modos de ejecución.

Para ambas ramas, solo se realizará una ejecución sencilla: no se creará ningun archivo adicional aparte de los csv procesados,
y un analisis de los datos en formato.txt
En rama_docker se incluye un Dockerfile para crear una imagen y un contenedor que aloje todo el proceso

En rama_dagster se da soporte a este orquestador para seguir todo el proceso
