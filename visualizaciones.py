# -- ------------------------------------------------------------------------------------ -- #
# -- proyecto: Microestructura y Sistemas de Trading - Laboratorio 2 - Behavioral Finance
# -- archivo: funciones.py - para visualizar loos datos.
# -- mantiene: Francisco Rodriguez
# -- repositorio:https://github.com/FranciscoRodRam/LAB_2_FRRR
# -- ------------------------------------------------------------------------------------ -- #


import funciones as fn
import plotly.express as px
import plotly.graph_objects as go

#Archivo a analizar
data = 'archivo_tradeview1.xlsx'



def pie(param_data):
    df_data = fn.f_leer_archivo(param_archivo=data)
    #columna de pips
    df_data = fn.f_columnas_pips(df_data)
    #Ranking de operaciones 
    df_1_ranking=fn.f_estadistica_ba2(param_data=df_data)
    df= df_1_ranking
    labels = df['simbolo']
    values = df['rank']
    pastel = go.Figure(data=[go.Pie(labels=labels, values=values, title='Ranking de Instrumentos', pull=[0.05, 0.05, 0, 0,0,0,0])])
    pastel.show()
    return pastel
