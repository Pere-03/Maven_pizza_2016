from xml.etree.cElementTree import Element, ElementTree, SubElement
from datetime import datetime
from plantilla_pdf import xml_to_pdf


def info_element(elemento_padre: Element, compañia: str, logo: str):

    info = SubElement(elemento_padre, 'info', company=compañia, logo = logo)


def titulo_element(elemento_padre: Element, titulo: str, fecha: str, autores: str):

    title = SubElement(elemento_padre, 'title', title=titulo, date=fecha, people=autores)


def imagen_element(elemento_padre: Element, nombre: str, imagen: str):

    image = SubElement(elemento_padre, 'imageslide', title=nombre, image=imagen)


def seccion_element(elemento_padre: Element, nombre_seccion: str):

    seccion = SubElement(elemento_padre, 'section', name=nombre_seccion)


def pagina_element(elemento_padre: Element, titulo: str, parrafo: str):

    pagina_normal = SubElement(elemento_padre, 'slide', title=titulo)

    for linea in parrafo.split('\n'):

        entrada = SubElement(pagina_normal, 'p')
        entrada.text = linea


def create_xml_presentation(semana):

    elem = Element('presentation')
    usuario = 'Alvaro Pereira, 202114948@alu.comillas.edu'
    info_element(elem, 'Maven Pizzas', 'logo.png')

    titulo = f'Ingredientes para la semana {semana}'
    titulo_element(elem, titulo, str(datetime.now().date()), usuario)

    seccion_element(elem, 'Analisis de los datasets entregados')

    texto = 'En esta seccion, vamos a hacer un análisis de los datos entregados, '
    texto += 'con vistas a pedir una mejora en la calidad de los mismos'
    texto += '\nExplicar los metodos empleados para la correcion de valores erróneos'
    pagina_element(elem, 'Objetivos', texto)

    imagen_element(elem, 'Datos erróneos para cada Dataset', 'analisis_datos.png')

    texto = 'Como podemos ver, 3 de los 5 datasets estaban impecables, pero tenemos ciertas quejas '
    texto += 'respecto a los datasets desarrollados por el personal (relacionados con los pedidos). '
    texto += 'En ellos, las fechas no seguian el estandar de la empresa, faltaban varias de ellas, '
    texto += 'los nombres de las pizzas no estaban bien escritos, habia cantidades en blanco o imposibles... '
    texto += 'Rogamos, para mejorar las predicciones futuras, que echeis un toque de atencion a los trabajadores.'
    pagina_element(elem, 'Peticion de mejora', texto)

    texto = 'Ante la gran falta de datos, hemos seguido los siguientes criterios:\n'
    texto += 'No hemos desechado ningún dato directamente, ya que si se registró algún pedido, '
    texto += 'será porque se ha pedido como poco una pizza. Esto sirve tanto para los pedidos vacíos, '
    texto += 'como para pedidos negativos (no existe política de reclamaciones en esta empresa).'
    texto += '\nEn cuanto a las fechas mal registradas, se ha decidido aceptar cualquier formato por esta vez. '
    texto += 'Como no empleabamos las horas, y ante el tiempo invertido para los puntos anteriores, '
    trxto += 'hemos decidio no emplear estos datos. '
    texto += 'No obstante, rogamos una mejora en ese aspecto, para poder situar mejor los pedidos en el tiempo.'
    texto += '\nPor último, nos sorprende haber visto nombres de pizzas erróneos. Hemos logrado "adivinar" '
    texto += 'La mayoria de ellas, pero no podemos seguir aceptando numeros o guiones en los nombres de las pizzas'
    pagina_element(elem, 'Toma de decisiones', texto)

    seccion_element(elem, 'Nuestra precicción para la semana')

    texto = f'Tal como se nos pidió, hemos hecho un análisis de la semana {semana}. '
    texto += 'En esta seccion, queremos hacer un añálisis de ingredientes pedidos en semanas similares '
    texto += 'Y entregar nuestros resutados, con un margen de error de +/- 4'
    pagina_element(elem, 'Objetivos', texto)

    texto = 'Vamos a mostrar una serie de gráficas que ayuden a la comprensión de la prediccion. '
    texto += f'De igual manera, se adjuntarán los archivos ingredientes_semana{semana} en formato xml y csv).'
    texto += '\nComo extra, mostraremos el ranking de pizzas más y menos pedidas, con vistas a alguna promocion '
    texto += 'o posibles cambios en la carta.'
    pagina_element(elem, 'Breve explicacion', texto)

    imagen_element(elem, 'Pedidos estimados de cada tipo de pizza', 'tipo_pedidos.png')

    imagen_element(elem, 'Cantidad de ingredientes necesarios', 'ingredientes.png')

    imagen_element(elem, 'Pizzas más pedidas', 'mejores_pizzas.png')

    imagen_element(elem, 'Pizzas menos pedidas', 'peores_pizzas.png')

    return elem


def crear_xml(nombre: str, semana: int):

    archivo = create_xml_presentation(str(semana))

    return archivo
    # ElementTree(archivo).write(nombre)


def crear_presentacion(nombre: str, semana: int):

    archivo = crear_xml(nombre, semana)

    xml_to_pdf(archivo, nombre)
