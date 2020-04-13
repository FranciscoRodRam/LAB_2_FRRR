# -- ------------------------------------------------------------------------------------ -- #
# -- proyecto: Microestructura y Sistemas de Trading - Laboratorio 2 - Behavioral Finance
# -- archivo: funciones.py - para visualizar loos datos.
# -- mantiene: Francisco Rodriguez
# -- repositorio:https://github.com/FranciscoRodRam/LAB_2_FRRR
# -- ------------------------------------------------------------------------------------ -- #

import funciones as fn
import plotly.express as px
import plotly.graph_objects as go
import os #Libreria orca,necesaria para crear las imagenes. 
#Archivo a analizar
data = 'archivo_tradeview1.xlsx'

# Función para crear gráfica con Pyplot 
def pie(param_data):
    #Se lee el archivo a graficar 
    df_data = fn.f_leer_archivo(param_archivo=data)
    #columna de pips
    df_data = fn.f_columnas_pips(df_data)
    #Se vuelve a crear el ranking 
    df_1_ranking=fn.f_estadistica_ba2(param_data=df_data)
    df= df_1_ranking
    labels = df['simbolo']
    values = df['rank']
    pastel = go.Figure(data=[go.Pie(labels=labels, values=values, pull=[0.05, 0.05, 0, 0,0,0,0],)])
    pastel.update_layout(title="Ranking de Instrumentos")
    pastel.show()

    #Se guarda la imagen con el objetivo de tener la visualización de la gráfica en Github
    if not os.path.exists("images"):
        os.mkdir("images")
    
    pastel.write_image("images/fig1.jpeg") #Guardar imagen 
    
    return pastel
