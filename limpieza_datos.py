import pandas as pd
from re import sub


def cambio_nan(nan):
    '''
    Como hay pedido, como poco tiene que haber 1 pizza
    '''
    try:
        nan = int(nan)
        if nan < 0:
            nan = -1*nan
        return nan

    except ValueError:
        return 1


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

    if '3' in pizza:
        pizza = sub('3', '3', pizza)

    return pizza


def arreglo_fechas(fecha: str):
    '''
    Convertiremos todas las fechas a formato Timestamp
    '''
    if not isinstance(fecha, str):

        return float('Nan')

    if '.' in fecha:

        return float('Nan')

    return pd.Timestamp(fecha).date()


def extract(pedidos='order_details.csv', fechas='orders.csv'):
    '''
    Extrae los 2 csv erroneos
    '''
    df_pedidos = pd.read_csv(f'./datasets/{pedidos}', sep=';', encoding='cp1252')
    df_fechas = pd.read_csv(f'./datasets/{fechas}', sep=';', encoding='cp1252')

    return df_pedidos, df_fechas


def transform(df_pedidos: pd.DataFrame, df_fechas: pd.DataFrame):
    '''
    Vamos a completar todos los datos incompletos/erróneos
    de los dataframes
    '''

    # Centremonos primero en el de los pedidos
    # Cambiamos los valores vacíos
    df_pedidos['quantity'] = df_pedidos['quantity'].apply(cambio_nan)
    df_pedidos = df_pedidos.fillna(method='ffill')

    # Y revisamos que las pizzas estén bien escritas
    df_pedidos['pizza_id'] = df_pedidos['pizza_id'].apply(revisar_pizzas)

    # Vayamos ahora a por el segundo dataframe
    # De este solo cambiaremos la fecha, y directamente eliminaremos las horas,
    # ya que no es un campo relevante para la prediccion
    df_fechas.pop('time')
    df_fechas['date'] = df_fechas['date'].apply(arreglo_fechas)
    df_fechas = df_fechas.fillna(method='bfill')

    return df_pedidos, df_fechas


def load(df_pedidos: pd.DataFrame, df_fechas: pd.DataFrame):
    '''
    Guardaremos ambos dataframes como un csv
    '''

    df_pedidos.to_csv('./datasets/order_details_corrected.csv')
    df_fechas.to_csv('./datasets/orders_corrected.csv')

    return df_pedidos, df_fechas


def main():
    '''
    Ejecuta todo el archivo
    '''
    load(*transform(*extract()))


if __name__ == '__main__':

    main()
