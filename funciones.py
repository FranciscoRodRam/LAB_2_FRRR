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
     # Elimninar -2 del nombre del instrumento
    df_data['symbol'] = [col.replace("-2", "") for col in df_data['symbol']]
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
    param_ins =  'archivo_tradeview_1.xlsx'
    """""    
    #jpy 100
    #usd 10,000
    #otro 10
    #lista de instrumentos con su multiplicador
    pips_inst =  {'xauusd': 10, 'eurusd': 10000, 'xaueur': 10,'bcousd':10000,
                  'cornusd':10000 ,'mbtcusd':10000,'wticousd':10000, 'spx500usd':10,
                  'audusd' : 10000, 'gbpusd': 10000,'xaueur':10, 'nas100usd':10,
                  'usdmxn': 10000, 'eurjpy':100,'gbpjpy':100, 'usdjpy':10000,
                  'btcusd':10000,'eurgbp':10, 'usdcad':10000}    
    return pips_inst[param_ins]

# -- ------------------------------------------------------ FUNCION: Transformaciones de tiempo  -- #
# -- ------------------------------------------------------------------------------------ -- #
# -- Agregar columnas de transformaciones de tiempo

def f_columnas_tiempos(param_data):
    """
    Parameters
    ----------
    param_data : 'archivo_tradeview_1'
    Returns
    -------
    datos
    Debugging
    ---------
    """
    param_data['closetime'] = pd.to_datetime(param_data['closetime'])
    param_data['opentime'] = pd.to_datetime(param_data['opentime'])
    #Tiempoo Transcurrido
    
    param_data['tiempo'] = [(param_data.loc[i, 'closetime'] - param_data.loc[i, 'opentime']).delta / 1*np.exp(9)

    for i in range(0, len(param_data['closetime']))]

    return param_data

# -- ------------------------------------------------------ FUNCION: Calcular pips -- #
# -- ------------------------------------------------------------------------------------ -- #
# --  Agregar con el cáluclo de pips
 
def f_columnas_pips(param_data):
    """
    Parameters
    ---------
    param_data: 'archivo_tradeview_1'
    Returns
    ------
    datos
    Debugging
    ------
    """
    param_data['pips'] = np.zeros(len(param_data['order']))
    param_data['pips_acm'] = np.zeros(len(param_data['order']))
    param_data['profit_acm'] = np.zeros(len(param_data['order']))    
    param_data['pips_acm'][0] = param_data['pips'][0]
    param_data['profit_acm'][0] = param_data['profit'][0]
    
    
    for i in range(0,len(param_data['order'])):
        #Compra
        pipsc =(param_data.closeprice[i] - param_data.openprice[i])*f_pip_size(param_ins=param_data['symbol'][i])
       #Venta
        pipsv =(param_data.openprice[i] - param_data.closeprice[i])*f_pip_size(param_ins=param_data['symbol'][i])
        if param_data['order'][i] == 'buy':
            param_data['pips'][i] = pipsc
        else:
            param_data['pips'][i] = pipsv
            
    for i in range(1,len(param_data['order'])):
        acumulador=param_data.pips_acm[i-1]+param_data.pips[i]
        acumulador2=param_data.profit_acm[i-1]+param_data.profit[i]
        param_data['pips_acm'][i]=acumulador
        param_data['profit_acm'][i]=acumulador2           
    return param_data



# -- ------------------------------------------------------ FUNCION: Calcular pips -- #
# -- ------------------------------------------------------------------------------------ -- #
# --  Agregar con el cáluclo de pips

def f_estadisticas_ba(param_data):
    """
    Parameters
    ----------
    param_data : 'archivo_tradeview_1.xlsx'
    Returns
    -------
    datos
    Debugging
    ---------
    """
    #Archivo para obtener la información estádistica 
    #param_data='archivo_tradeview_1.xlsx'
    diccionario= {'medida':
         ['Ops totales','Ganadoras','Ganadoras_c','Ganadoras_v','Perdedoras','Perdedoras_c','Perdedoras_v','Media(Profit)','Media(Pips)','r_efectividad','r_proporcion','r_efectividad_c','r_efectividad_v'],
         'valor':np.zeros(13),
         'descripcion':
         ['Operaciones totales','Operaciones ganadoras','Operaciones ganadoras de compra','Operaciones ganadoras de venta', 'Operaciones perdedoras','Operaciones perdedoras de compra',
          'Operaciones perdedoras de venta','Mediana profit de operaciones', 'Mediana de pips de operaciones', 'Ganadoras Totaes/Operaciones Totales', 'Perdedoras Totales/Operaciones Totales',
          'Ganadoras Compras/Operaciones Totales', 'Ganadoras Ventas/Operaciones Totales']
         }
    #DataFrame vacío. 
    df_tabla_1 = pd.DataFrame(diccionario)
    #Operaciones totales
    df_tabla_1['valor'][0]=len(param_data['type'])
    #Ganadoras
    df_tabla_1['valor'][1] = param_data['profit'].gt(0).sum()
    #Perdedoras
    df_tabla_1['valor'][4] = df_tabla_1['valor'][0] - df_tabla_1['valor'][1]
    #Media Profit
    df_tabla_1['valor'][7] = param_data.profit.median()
    #Media Pips
    df_tabla_1['valor'][8] = param_data.pips.median()
    
    w,x,y,z = 0,0,0,0
    
    for i in range(0,len(param_data['type'])): 
        #Ganadoras compra 
        if param_data['type'][i] == 'buy' and param_data['profit'][i] > 0 :
            w = w+1
        #Ganadoras venta
        if param_data['type'][i] == 'sell' and param_data['profit'][i] > 0 :
            x = x+1
        #Perdedoras compra
        if param_data['type'][i] == 'buy' and param_data['profit'][i] < 0 :
            y= y+1
        #Perdedoras_venta
        if param_data['type'][i] == 'sell' and param_data['profit'][i] < 0 :
            z = z+1
    #asignando los valores anteriormente calculados misma secuencia.
    df_tabla_1['valor'][2] = w
    df_tabla_1['valor'][3] = x
    df_tabla_1['valor'][5] = y
    df_tabla_1['valor'][6] = z 
    
    #r_efectividad
    df_tabla_1['valor'][9] = df_tabla_1['valor'][0] / df_tabla_1['valor'][1]
    #r_proporcion
    df_tabla_1['valor'][10] = df_tabla_1['valor'][1] / df_tabla_1['valor'][4]
    #r_efectividad_c
    df_tabla_1['valor'][11] = df_tabla_1['valor'][0] / df_tabla_1['valor'][2] 
    #r_efectivdad_v
    df_tabla_1['valor'][12] = df_tabla_1['valor'][0] / df_tabla_1['valor'][3] 
    
    
    return df_tabla_1

