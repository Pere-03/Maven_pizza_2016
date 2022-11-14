import pandas as pd
import re
import os
import requests
import plotly.graph_objects as go

from calidad_datos import main as analisis
from transformacion_datos import etl as transformar
from xml.etree.ElementTree import Element, ElementTree, SubElement
from reporte import crear_presentacion
from plantilla_excel import make_excel


ERROR = 4


def df_to_dict(dicc):

    tmp = {}

    for clave in dicc['Nº esperado'].keys():

        ingrediente = dicc['Ingrediente'][clave]

        ingrediente = re.sub(' ', '_', ingrediente)

        if ingrediente == '‘Nduja_Salami':
            ingrediente = 'Nduja_Salami'

        tmp[ingrediente] = dicc['Nº esperado'][clave]

    return tmp


def dict_to_xml(tag, d):

    elem = Element(tag)

    pedidos = SubElement(elem, 'Pedidos')

    ingredientes = SubElement(elem, 'Ingredientes')

    for key, val in d.items():

        if key != 'Pedidos':

            child = SubElement(ingredientes, 'Ingrediente', name=key, cantidad=str(val))

        else:

            child = SubElement(pedidos, 'Pedidos', cantidad=str(val))

    return elem


def crear_imagen(imag_name, x, y, color=None, customscale=None):

    fig = go.Figure()
    if customscale is not None:
        fig.add_trace(go.Bar(x=x, y=y, marker=dict(color=color, colorscale=customscale)))

    elif color is not None:
        fig.add_trace(go.Bar(x=x, y=y, marker=dict(color=color)))

    else:
        fig.add_trace(go.Bar(x=x, y=y))

    fig.write_image(f"imagenes/{imag_name}")


def crear_imagenes(df_ingredientes: pd.DataFrame, df_pizzas: pd.DataFrame, dicc: dict):

    contador = False
    for file in os.scandir('./'):
        if file.name == 'imagenes' and not contador:
            contador = True
    logo = False

    if not contador:
        os.mkdir('imagenes')

    for imagen in os.scandir('./imagenes/'):
        if imagen.name == 'logo.png' and not logo:
            logo = True

    if not logo:
        imagen = requests.get('https://img1.wsimg.com/isteam/ip/5a78177b-0605-4ae4-9d2a-c96dfa5cccbd/logo/9609391e-6d81-4d26-8a42-0d9aa201a919.jpg/:/rs=h:160/qt=q:95.png')
        code = open('./imagenes/logo.png', 'wb')
        code.write(imagen.content)

    dicc_sem = df_ingredientes.to_dict()

    ingredientes = []
    cantidades = []
    i = 0
    for value in dicc_sem.values():
        if not i:
            for value2 in value.values():
                i += 1
                if i > 1:
                    ingredientes.append(value2)
        else:
            for value2 in value.values():
                cantidades.append(value2)

    cantidades.pop(0)

    crear_imagen('ingredientes.png', x=ingredientes, y=cantidades)

    dicc_sem1 = df_pizzas[['pizza_type_id', 'Pedidos']].to_dict()

    pizzas = []
    pedidos = []

    for i in range(len(dicc_sem1['Pedidos']) - 1):

        pizzas.append(dicc_sem1['pizza_type_id'][i])
        pedidos.append(dicc_sem1['Pedidos'][i])

    crear_imagen('tipo_pedidos.png', x=pizzas, y=cantidades)

    maximo = [0]*5
    mayores = [0]*5

    minimo = [10000]*5
    menores = [0]*5

    for i in range(len(dicc_sem1['Pedidos']) - 1):

        cantidad = dicc_sem1['Pedidos'][i]
        pizza = dicc_sem1['pizza_type_id'][i]

        for max in range(5):

            if maximo[max] < cantidad and pizza not in mayores:

                maximo[max] = cantidad
                mayores[max] = pizza

        for min in range(5):

            if minimo[min] > cantidad and pizza not in menores:

                minimo[min] = cantidad
                menores[min] = pizza

    z1 = [max for max in maximo]
    z2 = [min for min in minimo]

    customscale = [
                [0, "rgb(128, 64, 0)"],
                [0.1, "rgb(205, 127, 50)"],
                [0.25, "rgb (128,128,128)"],
                [1.0, "rgb(255, 215, 0)"]
                ]

    crear_imagen('mejores_pizzas.png', x=mayores, y=maximo, color=z1, customscale=customscale)

    crear_imagen('peores_pizzas.png', x=menores, y=minimo, color=z2, customscale=customscale)

    ficheros = []
    valores = []
    for value in dicc.values():
        valor = 0
        for value2 in value['Contenidos'].values():
            valor += int(value2['Valores_Null_Nan'])

        ficheros.append(value['Nombre_fichero'])
        valores.append(valor)

    crear_imagen('analisis_datos.png', x=ficheros, y=valores, color='red')

    return


def aproximar_numero(numero: float):
    '''
    Aproxima un número, añadiéndole un margen de error
    '''

    global ERROR

    return int(round(numero) + ERROR)


def extract(semana: int):
    '''
    Recoge los datos del csv correspondiente a esa semana.
    sino, llamará a la anterior ETL
    '''

    nombre_csv = 'csv_procesado_semana' + str(semana) + '.csv'

    # Lo primero será ver si existe el archivo
    try:

        return pd.read_csv(f'./datasets/{nombre_csv}')

    # Sino, nos tocará extraer los datos de la otra ETL
    except FileNotFoundError:

        try:

            dataframe = transformar(semana)

            return dataframe

        except Exception as ex:

            print(f'Fallo causado por la excepcion {ex}')

            return False


def transform(dataframe: pd.DataFrame):
    '''
    Dividimos el dataframe por semanas
    '''

    if isinstance(dataframe, pd.DataFrame):

        df_ingredientes = dataframe.tail(1)

        df_ingredientes.pop('pizza_type_id')
        df_ingredientes.pop('size')

        df_ingredientes = df_ingredientes.apply(aproximar_numero)

        df_ingredientes = pd.DataFrame(df_ingredientes)
        df_ingredientes = df_ingredientes.rename(columns={'Unnamed: 0': 'Ingrediente', 0: 'Nº esperado'})

        return df_ingredientes, dataframe

    else:

        return False


def load(df: pd.DataFrame, df_pedidos: pd.DataFrame, dicc: dict, nombre: str):
    '''
    Guardaremos los ingredientes a comprar en un csv
    De igual manera, los imprimiremos por pantalla
    '''
    if isinstance(df, pd.DataFrame):

        conclusiones = False
        for file in os.scandir('./'):

            if file.name == 'conclusiones' and not conclusiones:
                conclusiones = True

        if not conclusiones:

            os.mkdir('conclusiones')

        df.to_csv(f'./conclusiones/{nombre}.csv')

        make_excel(df_pedidos, df, nombre)

        print(df)
        mensaje = f'Para más informacion, vaya a los siguientes archivos: '
        mensaje += f'{nombre}.csv, {nombre}.xlm, {nombre}.pdf, {nombre}.xlsx'
        print(mensaje)

        df = pd.read_csv(f'./conclusiones/{nombre}.csv')
        df = df.rename(columns={'Unnamed: 0': 'Ingrediente'})
        tmp = df.to_dict()

        tmp = df_to_dict(tmp)

        archivo = dict_to_xml(
                                'Semana_' +
                                re.sub('ingredientes_semana', '', nombre), tmp)

        ElementTree(archivo).write(f'./conclusiones/{nombre}.xml')

        crear_imagenes(df, df_pedidos, dicc)

        crear_presentacion(nombre, re.search('\d+', nombre).group())

        return df

    else:
        return False


def main(semana=-1):
    '''
    Ejecuta todo el programa en el siguiente orden:
    1) Hace un análisis de los datos > analisis_datos.txt
    2) Extrae los datos de otra ETL, que filtra los datos segun los meses
        indicados, guardando los pedidos (pizzas e ingredientes) en ese periodo
    3) Realiza un prediccion para ese mismo mes, semana por semana
    '''
    dicc = analisis()

    while 52 <= semana or semana < 0:
        try:
            semana = int(input('Inserte numero de semana del año: '))

        except ValueError:
            semana = -1

    nombre = 'ingredientes_semana' + str(semana)

    return load(*transform(extract(semana)), dicc, nombre)


if __name__ == '__main__':

    main()
