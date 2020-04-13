# -- ------------------------------------------------------------------------------------ -- #
# -- proyecto: Microestructura y Sistemas de Trading - Laboratorio 2 - Behavioral Finance
# -- archivo: funciones.py - para visualizar loos datos.
# -- mantiene: Francisco Rodriguez
# -- repositorio:https://github.com/FranciscoRodRam/LAB_2_FRRR
# -- ------------------------------------------------------------------------------------ -- #

import funciones as fn
import visualizaciones as vn

#Archivo a analizar.
data = 'archivo_tradeview1.xlsx'

#--Esta función corresponde a la lectura del archivo. 
df_data = fn.f_leer_archivo(param_archivo=data)
#funcion para conocer el mulplicador PIPS
pips = fn.f_pip_size(param_ins='cornusd')
#Columna de tiempo
df_data = fn.f_columnas_tiempos(param_data=df_data)
#columna de pips
df_data = fn.f_columnas_pips(df_data)
#Cálculo del capital acumulado 
df_data = fn.f_capital_acum(df_data)
#Sesgo
df_data = fn.sesgo(df_data)
#Extraer mes y día de la fecha 
df_data =fn.fechas(df_data)


#Estadística básica
df_1_tabla=fn.f_estadisticas_ba(param_data=df_data)
#Ranking de operaciones 
df_1_ranking=fn.f_estadistica_ba2(param_data=df_data)
df_1_ranking = df_1_ranking.reset_index(drop=True) 

#Condicional para llamar las funciones de acuerdo al archivo que se desea analizar. 

if data == 'archivo_tradeview1.xlsx':
    #Cáluclo del Profit diario 
    df_profit_diario = fn.profitdiario(param_data=df_data)
    profit_sinsabado=fn.sinsabado(param_data=df_data)
    f_estadistica_mad = fn.f_estadistica_mad(param_data=df_profit_diario)
    grafica_pastel = vn.pie(param_data=data)
    ratio= fn.inforatio(param_data=df_data)
    f_be_de=fn.f_be_de(param_data=df_data)
else:
    df_profit_diario = fn.profit2diario(param_data=df_data)
    profit_sinsabado=fn.sinsabado2(param_data=df_data)
    f_estadistica_mad = fn.f_estadistica2_mad(param_data=df_profit_diario)
    ratio = fn.inforatio2(param_data=df_data)
    grafica_pastel = vn.pie(param_data=data)
