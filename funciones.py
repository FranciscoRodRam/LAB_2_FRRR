<<<<<<< HEAD
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

    # Leer archivo
    df_data = pd.read_excel('archivos/' + param_archivo, sheet_name='Sheet1')

    # Elegir renglones type == buy | type == sell
    df_data = df_data[df_data.type != 'balance']

    # Resetear indice
    df_data = df_data.reset_index()

    # Convertir en minusculas los titulos de las columnas
    df_data.columns = [list(df_data.columns)[i].lower()
                       for i in range(0, len(df_data.columns))]

    # Asegurar ciertas columnas de tipo numerico
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

# -- ------------------------------------------------------ FUNCION:  -- #
# -- ------------------------------------------------------------------------------------ -- #
# --

def f_columnas_datos(param_data):
    """
    """
    # Convertir las columnas de closetime y opentime con to_datetime
    param_data['closetime'] = pd.to_datetime(param_data['closetime'])
    param_data['opentime'] = pd.to_datetime(param_data['opentime'])
    # Tiempo transcurrido de una operación
    param_data['tiempo'] = [(param_data.loc[i, 'closetime'] - param_data.loc[i, 'opentime']).delta / 1e9
                            for i in range(0, len(param_data['closetime']))]
    return param_data
# -- ------------------------------------------------------ FUNCION:  -- #
# -- ------------------------------------------------------------------------------------ -- #
# --
def f_columnas_pips(param_data):
    param_data['pips'] = np.zeros(len(param_data['type']))
    for i in range(0, len(param_data['type'])):
        if param_data['type'][i] == 'buy':
            param_data['pips'][i] = (param_data.closeprice[i] - param_data.openprice[i]) * f_pip_size(
                param_ins=param_data['symbol'][i])
        else:
            param_data['pips'][i] = (param_data.openprice[i] - param_data.closeprice[i]) * f_pip_size(
                param_ins=param_data['symbol'][i])
    return param_data

=======
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

    # Leer archivo
    df_data = pd.read_excel('archivos/' + param_archivo, sheet_name='Sheet1')

    # Elegir renglones type == buy | type == sell
    df_data = df_data[df_data.type != 'balance']

    # Resetear indice
    df_data = df_data.reset_index()

    # Convertir en minusculas los titulos de las columnas
    df_data.columns = [list(df_data.columns)[i].lower()
                       for i in range(0, len(df_data.columns))]

    # Asegurar ciertas columnas de tipo numerico
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

# -- ------------------------------------------------------ FUNCION:  -- #
# -- ------------------------------------------------------------------------------------ -- #
# --

def f_columnas_datos(param_data):
    """
    """
    # Convertir las columnas de closetime y opentime con to_datetime
    param_data['closetime'] = pd.to_datetime(param_data['closetime'])
    param_data['opentime'] = pd.to_datetime(param_data['opentime'])
    # Tiempo transcurrido de una operación
    param_data['tiempo'] = [(param_data.loc[i, 'closetime'] - param_data.loc[i, 'opentime']).delta / 1e9
                            for i in range(0, len(param_data['closetime']))]
    return param_data
# -- ------------------------------------------------------ FUNCION:  -- #
# -- ------------------------------------------------------------------------------------ -- #
# --
def f_columnas_pips(param_data):
    param_data['pips'] = np.zeros(len(param_data['type']))
    for i in range(0, len(param_data['type'])):
        if param_data['type'][i] == 'buy':
            param_data['pips'][i] = (param_data.closeprice[i] - param_data.openprice[i]) * f_pip_size(
                param_ins=param_data['symbol'][i])
        else:
            param_data['pips'][i] = (param_data.openprice[i] - param_data.closeprice[i]) * f_pip_size(
                param_ins=param_data['symbol'][i])
    return param_data

>>>>>>> 08dc83e60cf5d1d0532a0ec3fd2a9c56156661b2
