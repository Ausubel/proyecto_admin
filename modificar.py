import numpy as np
import pandas as pd

# Modificar DataFrame por tema
def mod_tema(tema, preguntas, df_cl):
    # Un arreglo con numpy para almacenar las claves
    arr_clave = np.array(df_cl['respuestas'])
    # Bucle para separar un string a una list
    for i in range(len(arr_clave)):
        if df_cl.iloc[i,1] == tema:
            str_clave = arr_clave[i]
            str_clave = list(str_clave)
    # Bucle para modificar las claves del arreglo
    for i in range(len(str_clave)):
        for j in range(len(preguntas)):
            if preguntas[j] == i + 1:
                str_clave[i] = ' '
    # Bucle para modificar el DataFrame
    for i in range(len(arr_clave)):
        if df_cl.iloc[i,1] == tema:
            arr_clave[i] = ''.join(str_clave)
            df_cl.iloc[i,2] = arr_clave[i]
    return f'El tema {tema}, ya se modifico.'

# Leer un string, tranformalo en list y en entero
def preguntas(cadena):
    # string a list
    cadena = list(cadena)
    # list(string) a int
    for i in range(len(cadena)):
        cadena[i] = int(cadena[i])
    return cadena