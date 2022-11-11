import pandas as pd
from typing import List
from xml.etree.ElementTree import Element, ElementTree


FICHEROS_CSV = [
            'data_dictionary.csv', 'order_details.csv',
            'orders.csv', 'pizza_types.csv', 'pizzas.csv']


diccionario = {}


def dict_to_xml(tag, d):

    elem = Element(tag)

    for key, val in d.items():

        if isinstance(val, dict):

            elem.append(dict_to_xml(key, val))

        else:

            child = Element(key)
            child.text = str(val)
            elem.append(child)

    return elem


def extract(fichero: str, sep=',') -> pd.DataFrame:
    '''
    Estraemos fichero.csv como un Dataframe
    '''
    dataframe = pd.read_csv(f'./datasets/{fichero}', sep=sep, encoding='cp1252')

    return dataframe


def transform(df: pd.DataFrame, fichero: str, i: int) -> str:
    '''
    Cogemos las columnas del dataframe y sus tipos, y
    analizamos cuantos Null/NaN hay en cada una de ellas.
    Devolvemos un string que contenga todos estos datos
    '''
    global diccionario

    mensaje = '\nEl fichero ' + fichero
    mensaje += ' contiene las siguientes columnas:\n\n'

    dicc = {}

    dicc['Nombre_fichero'] = fichero
    dicc['Contenidos'] = {}

    for colum in df.columns:

        dicc['Contenidos'][colum] = {}
        dicc['Contenidos'][colum]['Tipo_dato'] = str(df[colum].dtype)
        dicc['Contenidos'][colum]['Valores_Null_Nan'] = str(df[colum].isnull().sum())

        tmp = colum
        tmp += '    ' + str(df[colum].dtype)
        tmp += '    Valores Null/Nan = ' + str(df[colum].isnull().sum())
        mensaje += tmp + '\n'

    diccionario['Fichero_' + str(i)] = dicc

    return mensaje, dicc


def load(mensaje: str, diccionario: dict, fichero: str):
    '''
    Imprimimos mensaje en un fichero
    '''
    file = open(fichero, 'a')
    file.write(mensaje)
    file.close()
    archivo = dict_to_xml('Dataset', diccionario)

    ElementTree(archivo).write('analisis_datos.xml')

    return diccionario


def analisis_datos(ficheros: List[str], salida='analisis_datos.txt'):
    '''
    Analiza los datos de ficheros .csv
    Por ello, asumimos que los ficheros contenidos en ficheros
    cumplirán esta condicion
    '''

    file = open(salida, 'w')
    file.close()
    i = 0
    dicc = {}

    for fichero in ficheros:
        i += 1
        sep = ','

        if fichero in ['order_details.csv', 'orders.csv']:
            sep = ';'

        dicc[f'Fichero_{i}'] = load(*transform(extract(fichero, sep), fichero, i), salida)

    return dicc


def main(ficheros=None):
    '''
    Ejecuta todo el programa.
    Ideal para importarlo desde otros archivos
    '''
    global FICHEROS_CSV

    if not ficheros:

        ficheros = FICHEROS_CSV

    return analisis_datos(ficheros)
