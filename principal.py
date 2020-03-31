# -- ------------------------------------------------------------------------------------ -- #
# -- proyecto: Microestructura y Sistemas de Trading - Laboratorio 2 - Behavioral Finance
# -- archivo: funciones.py - para visualizar loos datos.
# -- mantiene: Francisco Rodriguez
# -- repositorio:https://github.com/FranciscoRodRam/LAB_2_FRRR
# -- ------------------------------------------------------------------------------------ -- #

import funciones as fn

df_data = fn.f_leer_archivo(param_archivo='archivo_tradeview_1.xlsx')

fn.f_pip_size(param_ins='cornusd')
df_data = fn.f_columnas_tiempos(param_data=df_data)
df_data = fn.f_columnas_pips(df_data)

df_1_tabla=fn.f_estadisticas_ba(param_data=df_data)
        
df_1_ranking=fn.f_estadistica_ba2(param_data=df_data)
