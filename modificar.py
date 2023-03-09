import numpy as np
import pandas as pd

def mod_tema(tema, preguntas, df_claves):
    list_preguntas = [int(i) for i in preguntas.split(',') if i != '']
    arr_clave = df_claves.loc[df_claves['tema_clave'] == tema, 'solucion'].apply(list).tolist()
    arr_clave = [char for solucion in arr_clave for char in solucion]
    for pregunta in list_preguntas:
        arr_clave[pregunta-1] = ' '
    return arr_clave