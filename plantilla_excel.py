import pandas as pd


def make_excel(df_pedidos: pd.DataFrame, df_ingredientes: pd.DataFrame, name):

    df_ingredientes = df_ingredientes.rename(
                                        columns={
                                            'Unnamed: 0': 'Ingrediente',
                                            0: 'Nº esperado'
                                            })
    try:
        df_ingredientes = df_ingredientes.drop(['Unnamed: 0', 'Pedidos'])
    except KeyError:
        pass

    df_pedidos['Pizzas'] = df_pedidos[['pizza_type_id', 'size']].apply(
                                                            ' '.join, axis=1
                                                                    )
    df_pedidos = df_pedidos[['Pizzas', 'Pedidos']]

    writer = pd.ExcelWriter(f'./conclusiones/{name}.xlsx', engine='xlsxwriter')

    max_row1 = df_ingredientes.shape[0]

    max_row2 = df_pedidos.shape[0]

    workbook = writer.book

    worksheet = workbook.add_worksheet('Reporte')

    df_pedidos.to_excel(
                    writer, sheet_name='Pedidos durante la semana',
                    index=False
                    )

    df_ingredientes.to_excel(
                    writer, sheet_name='Ingredientes a pedir',
                    index=True
                    )

    chart = workbook.add_chart({'type': 'column'})

    chart.add_series({
        'values': ['Pedidos durante la semana', 2, 1, max_row2 - 1, 1],
        'categories': ['Pedidos durante la semana', 2, 0, max_row2 - 1, 0]
    })

    chart.set_title({'name': 'Pedidos durante la semana'})
    chart.set_x_axis({'name': 'Tipo de pizza', 'num_font':  {'rotation': -45}})

    chart.set_y_axis({'name': 'Cantidad estimada'})
    chart.set_legend({'none': True})

    worksheet.insert_chart('A32', chart, {'x_scale': 4.5, 'y_scale': 2})

    chart1 = workbook.add_chart({'type': 'column'})

    chart1.add_series({
        'values': ['Ingredientes a pedir', 2, 1, max_row1, 1],
        'categories': ['Ingredientes a pedir', 2, 0, max_row1, 0],
        'data_labels': {'value': True}
    })

    chart1.set_title({'name': 'Ingredientes a pedir'})
    chart1.set_x_axis({'name': 'Tipo de ingrediente'})
    chart1.set_y_axis({'name': 'Cantidad a pedir'})
    chart1.set_legend({'none': True})

    worksheet.insert_chart('A1', chart1, {'x_scale': 2.75, 'y_scale': 2})

    writer.close()
