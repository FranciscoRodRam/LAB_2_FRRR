# -- ------------------------------------------------------------------------------------ -- #
# -- proyecto: Microestructura y Sistemas de Trading - Laboratorio 2 - Behavioral Finance
# -- archivo: funciones.py - para visualizar loos datos.
# -- mantiene: Francisco Rodriguez
# -- repositorio:https://github.com/FranciscoRodRam/LAB_2_FRRR
# -- ------------------------------------------------------------------------------------ -- #

import funciones as fn

df_data = fn.f_leer_archivo(param_archivo='archivo_tradeview_1.xlsx')

fn.f_pip_size(param_ins='cornusd')
datos = fn.f_columnas_tiempos(param_data=df_data)
datos = fn.f_columnas_pips(datos)

df_tabla_1=fn.f_estadisticas_ba(param_data=datos)
