# -- ------------------------------------------------------------------------------------ -- #
# -- proyecto: Microestructura y Sistemas de Trading - Laboratorio 2 - Behavioral Finance
# -- archivo: funciones.py para procesamiento de datos.
# -- mantiene: Francisco Rodriguez procesamiento de datos
# -- repositorio:https://github.com/FranciscoRodRam/LAB_2_FRRR
# -- ------------------------------------------------------------------------------------ -- #

import pandas as pd
# -- --------------------------------------------------- FUNCION: Leer archivo de entrada -- #
# -- ------------------------------------------------------------------------------------ -- #
# -- Importar el archivo.

def f_leer_archivo(param_archivo):
    """
    Parameters
    ----------
    param_archivo : str : nombre de archivo a leer
    Returns
    -------
    df_data : pd.DataFrame : con informacion contenida en archivo leido
    Debugging
    ---------
    """
    param_archivo = 'archivo_tradeview1.xlsx'

    # Leer archivo
    df_data = pd.read_excel('archivos/' + param_archivo, sheetname = 'Sheet1')
    # Elegir solo renglones en los que la columna type == 'buy' | type == 'sell'
    # Convertir en minúsculas el nombre de las columnas por si se encuentran en mayúsculas o mixtas
    df_data.columns = [list(df_data.columns)[i].lower() for i in list(df_data.columns)]
    numcols = ['s/l', 't/p', 'commission', 'openprice', 'closeprice', 'profit', 'size', 'swap', 'taxes', 'order']
    df_data[numcols] = df_data[numcols].apply(pd.to_numeric)

    return df_data

# -- ------------------------------------------------------ FUNCION: Pips por instrumento -- #
# -- ------------------------------------------------------------------------------------ -- #
# -- calcular el tamaño de los pips por instrumento



def f_pip_size(param_ins):
    """
    Parameters
    ----------
    param_ins : str : nombre de instrumento
    Returns
    -------
    Debugging
    -------
    param_ins = 'usdjpy'
    """
    # encontrar y eliminar un guion bajo
    # inst = param_ins.replace('_', '')
    # transformar a minusculas
    inst = param_ins.lower()
    # lista de pips por instrumento
    pips_inst = {







    }
    return pips_inst[inst]

def f_columnas_datos(param_data):
    """
    :param param_data: dataframe conteniendo por lo menos las columnas 'closetime' y 'opentime'
    :return: dataframe ingresado mas columna 'time' que es la diferencia entre close y open
    Debugging
    --------
    param_data = datos
    """
    # Convertir las columnas de closetime y opentime con to_datetime
    param_data['closetime'] = pd.to_datetime(param_data['closetime'])
    param_data['opentime'] = pd.to_datetime(param_data['opentime'])

    # Tiempo transcurrido de una operación

    param_data['tiempo'] = [(param_data.loc[i, 'closetime'] - param_data.loc[i, 'opentime']).delta / 1e9

                            for i in range(0, len(param_data['closetime']))]

    return param_data

