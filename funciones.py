# -- ------------------------------------------------------------------------------------ -- #

# -- proyecto: Microestructura y Sistemas de Trading - Laboratorio 2 - Behavioral Finance
# -- archivo: funciones.py para procesamiento de datos.
# -- mantiene: Francisco Rodriguez procesamiento de datos
# -- repositorio:https://github.com/FranciscoRodRam/LAB_2_FRRR
# -- ------------------------------------------------------------------------------------ -- #
import numpy as np
import pandas as pd
# -- --------------------------------------------------- FUNCION: Leer archivo de entrada -- #
# -- ------------------------------------------------------------------------------------ -- #
# -- Importar el archivo.
# %% FUNCION: leer archivo

def f_leer_archivo(param_archivo):

    """
    Funcion para leer archivo en formato xlsx.
    :param param_archivo: Cadena de texto con el nombre del archivo
    :return: dataframe de datos importados de archivo excel
    Debugging
    ---------
    param_archivo = 'archivo_tradeview_1.xlsx'
    """
 # Leer archivo de datos y guardarlo en Data Frame
    df_data = pd.read_excel('archivos/' + param_archivo, sheet_name='Sheet1')
   # Convertir a minusculas el nombre de las columnas
    df_data.columns = [list(df_data.columns)[i].lower() for i in range(0, len(df_data.columns))]
    # Asegurar que ciertas columnas son tipo numerico
    numcols =  ['s/l', 't/p', 'commission', 'openprice', 'closeprice', 'profit', 'size', 'swap', 'taxes']
    df_data[numcols] = df_data[numcols].apply(pd.to_numeric)    
    return df_data

# -- ------------------------------------------------------ FUNCION: Pips por instrumento -- #
# -- ------------------------------------------------------------------------------------ -- #
# -- calcular el tamaño de los pips por instrumento
def f_pip_size(param_ins):

    """"
    Parameters
    ----------
    param_ins : str : nombre de instrumento 
    Returns
    -------
    pips_inst : 
    Debugging
    ---------
    """""
    param_ins =  'archivo_tradeview_1.xlsx'
    # encontrar y eliminar un guion bajo
    inst = param_ins.replace('_', '')
    inst = param_ins.replace('-2', '')    
    # transformar a minusculas
    inst = inst.lower()
    #lista de pips por instrumento
    pips_inst =  {'xauusd': 10, 'eurusd': 10000, 'xaueur': 10,'bcousd':1000,'conrusd':10000 ,'mbtcusd':1000,'wtiusd':1000, 'spx500usd':10}
    
    return pips_inst[param_ins]

# -- ------------------------------------------------------ FUNCION:  -- #
# -- ------------------------------------------------------------------------------------ -- #
# -- convertir columna de 'closetime' y 'opentime' utilizando pd.to_datetime

def f_columnas_tiempo(param_data):

    param_data['closetime'] = pd.to_datetime(param_data['closetime'])
    param_data['opentime'] = pd.to_datetime(param_data['opentime'])
    param_data['tiempo'] = [(param_data.loc[i, 'closetime'] - param_data.loc[i, 'opentime']).delta / 1*np.exp(9)
    for i in range(0, len(param_data['closetime']))]
    return param_data