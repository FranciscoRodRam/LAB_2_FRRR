# -- ------------------------------------------------------------------------------------ -- #

# -- proyecto: Microestructura y Sistemas de Trading - Laboratorio 2 - Behavioral Finance
# -- archivo: funciones.py para procesamiento de datos.
# -- mantiene: Francisco Rodriguez procesamiento de datos
# -- repositorio:https://github.com/FranciscoRodRam/LAB_2_FRRR
# -- ------------------------------------------------------------------------------------ -- #
import numpy as np
import pandas as pd
from datetime import timedelta                            # diferencia entre datos tipo tiempo
from oandapyV20 import API                                # conexion con broker OANDA
import oandapyV20.endpoints.instruments as instruments    # informacion de precios historicos
from datos import OA_Ak           

# -- --------------------------------------------------------- FUNCION: Descargar precios -- #
# -- Descargar precios historicos con OANDA

def f_precios_masivos(p0_fini, p1_ffin, p2_gran, p3_inst, p4_oatk, p5_ginc):
    """
    Parameters
    ----------
    p0_fini
    p1_ffin
    p2_gran
    p3_inst
    p4_oatk
    p5_ginc

    Returns
    -------
    dc_precios

    Debugging
    ---------

    """

    def f_datetime_range_fx(p0_start, p1_end, p2_inc, p3_delta):
        """

        Parameters
        ----------
        p0_start
        p1_end
        p2_inc
        p3_delta

        Returns
        -------
        ls_resultado

        Debugging
        ---------
        """

        ls_result = []
        nxt = p0_start

        while nxt <= p1_end:
            ls_result.append(nxt)
            if p3_delta == 'minutes':
                nxt += timedelta(minutes=p2_inc)
            elif p3_delta == 'hours':
                nxt += timedelta(hours=p2_inc)
            elif p3_delta == 'days':
                nxt += timedelta(days=p2_inc)

        return ls_result

    # inicializar api de OANDA

    api = API(access_token=p4_oatk)

    gn = {'S30': 30, 'S10': 10, 'S5': 5, 'M1': 60, 'M5': 60 * 5, 'M15': 60 * 15,
          'M30': 60 * 30, 'H1': 60 * 60, 'H4': 60 * 60 * 4, 'H8': 60 * 60 * 8,
          'D': 60 * 60 * 24, 'W': 60 * 60 * 24 * 7, 'M': 60 * 60 * 24 * 7 * 4}

    # -- para el caso donde con 1 peticion se cubran las 2 fechas
    if int((p1_ffin - p0_fini).total_seconds() / gn[p2_gran]) < 4999:

        # Fecha inicial y fecha final
        f1 = p0_fini.strftime('%Y-%m-%dT%H:%M:%S')
        f2 = p1_ffin.strftime('%Y-%m-%dT%H:%M:%S')

        # Parametros pra la peticion de precios
        params = {"granularity": p2_gran, "price": "M", "dailyAlignment": 16, "from": f1,
                  "to": f2}

        # Ejecutar la peticion de precios
        a1_req1 = instruments.InstrumentsCandles(instrument=p3_inst, params=params)
        a1_hist = api.request(a1_req1)

        # Para debuging
        # print(f1 + ' y ' + f2)
        lista = list()

        # Acomodar las llaves
        for i in range(len(a1_hist['candles']) - 1):
            lista.append({'TimeStamp': a1_hist['candles'][i]['time'],
                          'Open': a1_hist['candles'][i]['mid']['o'],
                          'High': a1_hist['candles'][i]['mid']['h'],
                          'Low': a1_hist['candles'][i]['mid']['l'],
                          'Close': a1_hist['candles'][i]['mid']['c']})

        # Acomodar en un data frame
        r_df_final = pd.DataFrame(lista)
        r_df_final = r_df_final[['TimeStamp', 'Open', 'High', 'Low', 'Close']]
        r_df_final['TimeStamp'] = pd.to_datetime(r_df_final['TimeStamp'])

        return r_df_final

    # -- para el caso donde se construyen fechas secuenciales
    else:

        # hacer series de fechas e iteraciones para pedir todos los precios
        fechas = f_datetime_range_fx(p0_start=p0_fini, p1_end=p1_ffin, p2_inc=p5_ginc,
                                     p3_delta='minutes')

        # Lista para ir guardando los data frames
        lista_df = list()

        for n_fecha in range(0, len(fechas) - 1):

            # Fecha inicial y fecha final
            f1 = fechas[n_fecha].strftime('%Y-%m-%dT%H:%M:%S')
            f2 = fechas[n_fecha + 1].strftime('%Y-%m-%dT%H:%M:%S')

            # Parametros pra la peticion de precios
            params = {"granularity": p2_gran, "price": "M", "dailyAlignment": 16, "from": f1,
                      "to": f2}

            # Ejecutar la peticion de precios
            a1_req1 = instruments.InstrumentsCandles(instrument=p3_inst, params=params)
            a1_hist = api.request(a1_req1)

            # Para debuging
            print(f1 + ' y ' + f2)
            lista = list()

            # Acomodar las llaves
            for i in range(len(a1_hist['candles']) - 1):
                lista.append({'TimeStamp': a1_hist['candles'][i]['time'],
                              'Open': a1_hist['candles'][i]['mid']['o'],
                              'High': a1_hist['candles'][i]['mid']['h'],
                              'Low': a1_hist['candles'][i]['mid']['l'],
                              'Close': a1_hist['candles'][i]['mid']['c']})

            # Acomodar en un data frame
            pd_hist = pd.DataFrame(lista)
            pd_hist = pd_hist[['TimeStamp', 'Open', 'High', 'Low', 'Close']]
            pd_hist['TimeStamp'] = pd.to_datetime(pd_hist['TimeStamp'])

            # Ir guardando resultados en una lista
            lista_df.append(pd_hist)

        # Concatenar todas las listas
        r_df_final = pd.concat([lista_df[i] for i in range(0, len(lista_df))])

        # resetear index en dataframe resultante porque guarda los indices del dataframe pasado
        r_df_final = r_df_final.reset_index(drop=True)

        return r_df_final

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
    #fecha de cierre
    param_data['closetime'] = pd.to_datetime(param_data['closetime'])
    #fehca de apertura
    param_data['opentime'] = pd.to_datetime(param_data['opentime'])

    # tiempo transcurrido de una operación
    param_data['tiempo'] = [(param_data.loc[i, 'closetime'] -
                             param_data.loc[i, 'opentime']).delta / 1e9
                            for i in range(0, len(param_data['closetime']))]

    # return param_data['tiempo']
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
    #Profit Acumulado
    for i in range(1,len(param_data['order'])):
        acumulador=param_data.pips_acm[i-1]+param_data.pips[i]
        acumulador2=param_data.profit_acm[i-1]+param_data.profit[i]
        param_data['pips_acm'][i]=acumulador
        param_data['profit_acm'][i]=acumulador2           
    return param_data



# -- ------------------------------------------------------ FUNCION: Estadisitica Básica -- #
# -- ------------------------------------------------------------------------------------ -- #
# --  Data Frame con Valores estadísticos.

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
    df_1_tabla = pd.DataFrame(diccionario)
    #Operaciones totales
    df_1_tabla['valor'][0]=len(param_data['type'])
    #Ganadoras
    df_1_tabla['valor'][1] = param_data['profit'].gt(0).sum()
    
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
    df_1_tabla['valor'][2] = w
    df_1_tabla['valor'][3] = x
    #Perdedoras
    df_1_tabla['valor'][4] = df_1_tabla['valor'][0] - df_1_tabla['valor'][1]
    df_1_tabla['valor'][5] = y
    df_1_tabla['valor'][6] = z 
    
     #Media Profit
    df_1_tabla['valor'][7] = param_data.profit.median()
    #Media Pips
    df_1_tabla['valor'][8] = param_data.pips.median()
    #r_efectividad
    df_1_tabla['valor'][9] = round((df_1_tabla['valor'][1]/ df_1_tabla['valor'][0]),2)
    #r_proporcion
    df_1_tabla['valor'][10] = round(df_1_tabla['valor'][1]/ df_1_tabla['valor'][4],2)
    #r_efectividad_c
    df_1_tabla['valor'][11] = round(df_1_tabla['valor'][2]/ df_1_tabla['valor'][0],2)
    #r_efectivdad_v
    df_1_tabla['valor'][12] = round( df_1_tabla['valor'][3]/df_1_tabla['valor'][0],2) 
    
    
    return df_1_tabla


# -- ------------------------------------------------------ FUNCION: Ranking -- #
# -- ------------------------------------------------------------------------------------ -- #
# --  Data Frame del ranking  con ratio de efectividad

def f_estadistica_ba2(param_data):
    """
    Parameters
    ----------
    param_data : 'archivo_tradeview1.xlsx'
    Returns
    -------
    datos
    Debugging
    ---------
    """
    #Archivo para obtener el ranking
    #param_data='archivo_tradeview_1.xlsx'
    
    #Simbolos utilizados en los diferentes archivos
    simbolos = ['xauusd','eurusd', 'xaueur','bcousd','cornusd','mbtcusd','wticousd', 'spx500usd',
                 'audusd', 'gbpusd','xaueur', 'nas100usd','usdmxn', 'eurjpy','gbpjpy', 'usdjpy',
                 'btcusd','eurgbp', 'usdcad']
    
    diccionario = {'simbolo':np.zeros(len(simbolos)),
                   'rank':np.zeros(len(simbolos))}
    #DataFrame vacío. 
    df_1_ranking = pd.DataFrame(diccionario)
    
    #Ciclo para crear ranking utilizando filtros
    for i in range(len(df_1_ranking)):
        filtro0 = param_data['symbol']==simbolos[i]
        filtro1 = param_data[filtro0]
        if filtro1.empty == False:
            filtro1 = param_data[filtro0]
            filtro2 = param_data[(param_data['symbol']==simbolos[i]) & (param_data['profit']>=0)]
            #Efectividad
            df_1_ranking['rank'][i]=round(len(filtro2)/len(filtro1),4)*100
            df_1_ranking['simbolo'][i]=simbolos[i]
        else:
            df_1_ranking['rank'][i]="nan"
        pass
    #ordenar de mayor a menor
    df_1_ranking =df_1_ranking.sort_values(by=['rank'],ascending=[False])
    #elimnando los valores vacíos del DataFrame creado inicialmente
    df_1_ranking =df_1_ranking.dropna()
    #Eliminar indices innecesarios
    

    return df_1_ranking

# -- ------------------------------------------------------ FUNCION: Capital acumulado -- #
# -- ------------------------------------------------------------------------------------ -- #
# --  Se anexa la columna de capital acumulado. 

def f_capital_acum(param_data):
    """
    Parameters
    ----------
    param_data : 'archivo_tradeview1.xlsx'
    Returns
    -------
    datos
    Debugging
    ---------
    """
 
    param_data['capital_acm'] = np.zeros(len(param_data['type']))
    param_data['capital_acm'][0] = 5000 + param_data['profit'][0]
            
    for i in range(1,len(param_data['pips'])):
         param_data['capital_acm'][i] = param_data['capital_acm'][i-1] + param_data['profit'][i]

    return param_data  


# -- ------------------------------------------------------ FUNCION para separar fechas -- #
# -- ------------------------------------------------------------------------------------ -- #
# -- Columnas en donde se extrae tanto el día como la fecha, se realiza para no afectar  -- #
# -- futuros cálculos-------------------------------------------------------------------- --    
        
def fechas(param_data):
    
    param_data['meses_close']=np.zeros(len(param_data['closetime']))
    param_data['dias_close']= np.zeros(len(param_data['closetime']))

    for i in range (len(param_data['closetime'])):
        param_data['dias_close'][i]=param_data['closetime'][i].day
    
    for i in range(len(param_data['opentime'])):
        param_data['meses_close'][i]=param_data['closetime'][i].month
        
    return param_data

# -- ------------------------------------------------------ FUNCION: Profit diario -- #
# -- ------------------------------------------------------------------------------------ -- #
# -- Función para cualcular el profit diario solamente para archivo_tradeview1


def profitdiario(param_data):
    """
    Parameters
    ----------
    param_data : 'archivo_tradeview1.xlsx'
    Returns
    -------
    datos
    Debugging
    ---------
    """
    data = param_data
    #Fecha del primer movimiento
    finicial = data['closetime'][0].date()
    #fecha del último movimiento
    ffinal =data['closetime'][len(param_data['closetime'])-1].date()
    
    #Diferencia para calcular la cantidad de días
    dif = (ffinal-finicial).days+8

    diccionario = {'timestamp':np.zeros(dif),
                   'profit_d':np.zeros(dif),
                   'profit_acm_d':np.zeros(dif)}
    #DataFrame 
    f_profit_diario = pd.DataFrame(diccionario)
    
    f_profit_diario['timestamp']=pd.date_range(start=finicial,periods=dif, freq='D')
    dias = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32]
    mes = [1,2,3,4,5,6,7,8,9,10,11,12]
    j=1 # primer mes 
    i=10 #primer día 
    k=0
    
    if k<=31:
        for k in range (len(f_profit_diario['timestamp'])):
            filtro1=(data[(data['meses_close']==mes[j]) & (data['dias_close']==dias[i])])  
            f_profit_diario['profit_d'][k]= filtro1['profit'].sum()
            i=i+1
            
    
    f_profit_diario['profit_acm_d'][0]=5000+f_profit_diario['profit_d'][0]
    i=1
    j=1
    for i in range(len(f_profit_diario)-1):
        f_profit_diario['profit_acm_d'][j]=f_profit_diario['profit_acm_d'][j-1]+f_profit_diario['profit_d'][j]
        j=j+1
        
    

    return f_profit_diario

# -- ------------------------------------------------------ FUNCION: Eliminar los sábados -- #
# -- ------------------------------------------------------------------------------------ -- #
# -- Eliminar el sábado,se asignará un nuevo DataFrame (principal) para no afectar futuros cálculos

def sinsabado(param_data):
    """
    Parameters
    ----------
    param_data : 'archivo_tradeview1.xlsx'
    Returns
    -------
    datos
    Debugging
    ---------
    """
    data = profitdiario(param_data)
    
        
    f_profit_diario = data[data.timestamp.dt.weekday != 5]
    
    return f_profit_diario
# -- ------------------------------------------------------ FUNCION: Profit diario -- #
# -- ------------------------------------------------------------------------------------ -- #
# -- Función para cualcular el profit diario solamente para archivo_tradeview_1

def profit2diario(param_data):
    
    """
    Parameters
    ----------
    param_data : 'archivo_tradeview1.xlsx'
    Returns
    -------
    datos
    Debugging
    ---------
    """
    
    data = param_data
    #Fecha del primer movimiento
    finicial = data['closetime'][0].date()
    #fecha del último movimiento
    ffinal =data['closetime'][len(param_data['closetime'])-1].date()
    
    #Diferencia para calcular la cantidad de días
    dif = (ffinal-finicial).days+2

    diccionario = {'timestamp':np.zeros(dif),
                   'profit_d':np.zeros(dif),
                   'profit_acm_d':np.zeros(dif)}
    #DataFrame 
    f_profit_diario = pd.DataFrame(diccionario)
    f_profit_diario['timestamp']=pd.date_range(start=finicial,periods=dif, freq='D')
    dias = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32]
    mes = [1,2,3,4,5,6,7,8,9,10,11,12]

    i=26 #primer día 
    l=0

    if data['meses_close'][l] == 8 and i<=31:
        for l in range (len(f_profit_diario['timestamp'])):
            if i<=31:
                filtro1=(data[(data['meses_close']==mes[7]) & (data['dias_close']==dias[i])])  
                f_profit_diario['profit_d'][l]= filtro1['profit'].sum()
                i=i+1
                l=l+1
    a=14 #dia
    h=1

    if data['meses_close'][a]==9 and h<=31:
        for a in range (6,len(f_profit_diario['timestamp'])):
            if h<=31:
                filtro1=(data[(data['meses_close']==mes[8]) & (data['dias_close']==dias[h])])  
                f_profit_diario['profit_d'][a]= filtro1['profit'].sum()
                h=h+1
                
    f_profit_diario['profit_acm_d'][0]=5000+f_profit_diario['profit_d'][0]
    i=1
    j=1
    for i in range(len(f_profit_diario)-1):
        f_profit_diario['profit_acm_d'][j]=f_profit_diario['profit_acm_d'][j-1]+f_profit_diario['profit_d'][j]
        j=j+1
    
    return f_profit_diario


# -- ------------------------------------------------------ FUNCION: Eliminar los sábados -- #
# -- ------------------------------------------------------------------------------------ -- #
# -- Eliminar el sábado,se asignará un nuevo DataFrame (principal) para no afectar futuros cálculos

def sinsabado2(param_data):
    
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
    data = profitdiario(param_data)
    
        
    f_profit_diario = data[data.timestamp.dt.weekday != 5]    
    
    return f_profit_diario

# -- ------------------------------------------------------ FUNCION: Info Ratio  -- #
# -- ------------------------------------------------------------------------------------ -- #
# -- Función para descargar precios masivos y calcular media del ratio 
    
def inforatio(param_data):
    OA_Gn = "D"                        # Granularidad de velas
    OA_In = "SPX500_USD"
    fi = "2020-02-12 00:00:00"      #Cambiar la fecha según el archivo a analizar
    ff   =  "2020-03-01 00:00:00"    #Cambuar la fecha según corresponda 
    fini = pd.to_datetime(fi).tz_localize('GMT')  # Fecha inicial
    ffin = pd.to_datetime(ff).tz_localize('GMT')  # Fecha
    df_pe = f_precios_masivos(p0_fini=fini, p1_ffin=ffin, p2_gran=OA_Gn,p3_inst=OA_In, p4_oatk=OA_Ak, p5_ginc=4900)    
    rend=[]
    
    for i in range(len(df_pe)-1):
        rlog=np.log((float(df_pe['Close'][i+1])/(float(df_pe['Close'][i]))))
        rend.append(rlog)  
   
    return rend



# -- ------------------------------------------------------ FUNCION: Info Ratio  -- #
# -- ------------------------------------------------------------------------------------ -- #
# -- Función para descargar precios masivos y calcular media del ratio 



# -- ------------------------------------------------------ FUNCION: Métricas de desempeño -- #
# -- ------------------------------------------------------------------------------------ -- #
# -- Función para cualcular métricas de desempeño solamente para archivo_tradeview1


def f_estadistica_mad(param_data):
    """
    Parameters
    ----------
    param_data : 'df_profit_diario'
    Returns
    -------
    datos
    Debugging
    ---------
    """
    
    #Elementos del DataFrame
    diccionario= {'metrica':
         ['Sharpe','Sortino_c','Sortino_v','Drawdown_capi','Drawup_capi','Information_r'],
         'valor':np.zeros(6),
         'descripcion':
         ['Sharpe Ratio','Sortino para posiciones compra', 'Sortino para posiciones venta' ,'DrawDown de capital', 'DrawUp de capital','Information_ratio']
         }
    #DataFrame vacío
    f_estadistica_mad = pd.DataFrame(diccionario)
    #Tasa libre de riesgo. 
    rf = 0.08/360
    #Minimum Acceptable Return
    mar = .30/300
    rendimientos=[]
    

    #Cálculos para el Sharpe 
    for i in range(len(param_data)-1):
        rendlog=np.log((param_data['profit_acm_d'][i+1]/param_data['profit_acm_d'][i]))
        rendimientos.append(rendlog)
    #rendimiento esperado        
    rendlog=np.mean(rendimientos)
    #desviación estándar
    desvest=np.std(rendimientos)
    #Sharpe     
    sharpe = (rendlog-rf)/desvest
    f_estadistica_mad['valor'][0]=sharpe
    
    #Sortino 

    f_estadistica_mad['valor'][1]="Pendiente"
    f_estadistica_mad['valor'][2]="Pendiente"
   

   #drawdown_capi
    
    minimo= (param_data['profit_acm_d'].min()) #Minusvalía mínima del histórico 
    fechai = str(param_data['timestamp'][0].date()) #fecha correspondiente de la minusvalía mínima
    maximo = (param_data['profit_acm_d'][0])   #máximo antes de la minusvalía mínima 
    fechaf = str(param_data['timestamp'][7].date()) #fecha correspondiente del máximo antes de la minusvalía mínima 
    drawdown = '%.2f'%(maximo-minimo)
    drawdown = str(drawdown)
    f_estadistica_mad['valor'][3]= fechai + " | " + fechaf + " | " + "$ " + drawdown #colocando el valor correspondiente. 
    
    #drawup_capi 
    
    maxim = (param_data['profit_acm_d'].max()) #Plusvalía máxima. 
    fechaff = str(param_data['timestamp'][15].date()) #fecha correspondiene al máximo del histórico
    drawup = '%.2f'%(maxim-minimo) 
    drawup = str(drawup)
    f_estadistica_mad['valor'][4]= fechaf + " | " + fechaff + " | " + "$ " + drawup #colocando el valor correspondiente. 
    
     
    #rendimiento esperado        
    rendslogratio=np.mean(inforatio(param_data))

    descuento = rendimientos -rendslogratio
    descuento = np.std(descuento)
    #Iformation Ratio     
    ratio= (rendlog-rendslogratio)/descuento
    f_estadistica_mad['valor'][5]=str(ratio)
        
   
    return f_estadistica_mad

# -- ------------------------------------------------------ FUNCION: Métricas de desempeño -- #
# -- ------------------------------------------------------------------------------------ -- #
# -- Función para cualcular métricas de desempeño solamente para archivo_tradeview_1

def f_estadistica2_mad(param_data):
    """
    Parameters
    ----------
    param_data : 'df_profit_diario'
    Returns
    -------
    datos
    Debugging
    ---------
    """
    
    #Elementos del DataFrame
    diccionario= {'metrica':
         ['Sharpe','Sortino_c','Sortino_v','Drawdown_capi','Drawup_capi','Information_r'],
         'valor':np.zeros(6),
         'descripcion':
         ['Sharpe Ratio','Sortino para posiciones compra', 'Sortino para posiciones venta' ,'DrawDown de capital', 'DrawUp de capital','Information_ratio']
         }
    #DataFrame vacío
    f_estadistica2_mad = pd.DataFrame(diccionario)
    #Tasa libre de riesgo. 
    rf = 0.08/360
    #Minimum Acceptable Return
    mar = 0.30/300
    
    rendimientos=[]
    sort=[]

    #Cálculos para el Sharpe 
    for i in range(len(param_data)-1):
        rendlog=np.log((param_data['profit_acm_d'][i+1]/param_data['profit_acm_d'][i]))
        rendimientos.append(rendlog)
    #rendimiento esperado        
    rendlog=np.mean(rendimientos)
    #desviación estándar
    desvest=np.std(rendimientos)
    #Sharpe     
    sharpe = (rendlog-rf)/desvest
    f_estadistica2_mad['valor'][0]=sharpe
    
    #Sortino 
    #Posiciones Compra
    
    
    #Posiciones Venta 
    #  
    
    
    #drawdown_capi
    
    minimo= (param_data['profit_acm_d'].min()) #Minusvalía mínima del histórico 
    fechai = str(param_data['timestamp'][1].date()) #fecha correspondiente de la minusvalía mínima
    maximo = (param_data['profit_acm_d'][1])   #máximo antes de la minusvalía mínima 
    fechaf = str(param_data['timestamp'][7].date()) #fecha correspondiente del máximo antes de la minusvalía mínima 
    drawdown = '%.2f'%(maximo-minimo)
    drawdown = str(drawdown)
    f_estadistica2_mad['valor'][3]= fechai + " | " + fechaf + " | " + "$ " + drawdown #colocando el valor correspondiente. 
    
    #drawup_capi 
    
    maxim = (param_data['profit_acm_d'].max()) #Plusvalía máxima. 
    fechaff = str(param_data['timestamp'][29].date()) #fecha correspondiene al máximo del histórico
    drawup = '%.2f'%(maxim-minimo) 
    drawup = str(drawup)
    f_estadistica2_mad['valor'][4]= fechaf + " | " + fechaff + " | " + "$ " + drawup #colocando el valor correspondiente. 
    


    
    return f_estadistica2_mad
    
