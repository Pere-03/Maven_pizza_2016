import pandas as pd
from re import sub


def cambio_nan(nan):
    '''
    Como hay pedido, como poco tiene que haber 1 pizza
    '''

    return nan if isinstance(nan, int) else 1


def revisar_pizzas(pizza):
    '''
    Comprueba los fallos más comunes a la hora de
    escribir un pedido
    '''
    separadores = ['-', ' ']

    for separador in separadores:

        if separador in pizza:

            pizza = sub(separador, '_', pizza)

    if '@' in pizza:

        pizza = sub('@', 'a', pizza)

    if '0' in pizza:

        pizza = sub('0', 'o', pizza)

    return pizza


def extract(pedidos='order_details.csv', fechas='orders.csv'):
    '''
    Extrae los 2 csv erroneos
    '''
    df_pedidos = pd.read_csv(pedidos, sep=';', encoding='cp1252')
    df_fechas = pd.read_csv(fechas, sep=';', encoding='cp1252')

    return df_pedidos, df_fechas


def transform(df_pedidos: pd.DataFrame, df_fechas: pd.DataFrame):
    '''
    Vamos a completar todos los datos incompletos/erróneos
    de los dataframes
    '''

    # Centremonos primero en el de los pedidos
    # Cambiamos los valores 
    df_pedidos['quantity'] = df_pedidos['quantity'].apply(cambio_nan)
    df_pedidos = df_pedidos.fillna(method='ffill')
    df_pedidos['pizza_id'] = df_pedidos['pizza_id'].apply(revisar_pizzas)


def load():
    pass


def main():
    pass


if __name__ == '__main__':

    main()
