# Maven_pizza_2016

Maven_pizza pero con datos erróneos
Haremos un filtrado de los datos antes de realizar el mismo proceso que en maven_pizza

Para ello, hemos de ejecutar el archivo python predictions.py

En esta rama podemos crearnos una imagen y un contenedor de docker que ejecute el proceso

Para crear la imagen, hemos de ejecutar "docker build -t nombre_imagen ." en el directorio donde tengamos todos los archivos.

Posteriormente, ejecutamos "docker run -it --name nombre_contenedor -v tu_path_absoluto:/usr/src/app nombre_imagen"
