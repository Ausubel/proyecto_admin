import numpy as np
import pandas as pd

with open('D:/proyecto_admin/proyecto_admin/identifi.sdf', 'r') as arc_identifi:
    array_identifi = arc_identifi.readlines()

with open('D:/proyecto_admin/proyecto_admin/respuestas.sdf', 'r') as arc_respuestas:
    array_respuestas = arc_respuestas.readlines()

with open('D:/proyecto_admin/proyecto_admin/claves.sdf', 'r') as arc_claves:
    array_claves = arc_claves.readlines()

df_identifi = pd.DataFrame(columns=['litho', 'tema', 'codigo'], index=range(len(array_identifi)))
df_respuestas = pd.DataFrame(columns=['litho', 'tema', 'respuestas'], index=range(len(array_respuestas)))
df_claves = pd.DataFrame(columns=['litho', 'tema', 'respuestas'], index=range(len(array_claves)))

for i in range(len(array_identifi)):
    litho_id = array_identifi[i][:6]
    tema_id = array_identifi[i][6]
    cod_id = array_identifi[i][7:13]
    df_identifi.iloc[i] = [litho_id, tema_id, cod_id]

for i in range(len(array_respuestas)):
    litho_re = array_respuestas[i][:6]
    tema_re = array_respuestas[i][6]
    respuestas_re = array_respuestas[i][7:107]
    df_respuestas.iloc[i] = [litho_re, tema_re, respuestas_re]

for i in range(len(array_claves)):
    litho_cl = array_claves[i][:6]
    tema_cl = array_claves[i][6]
    respuestas_cl = array_claves[i][7:107]
    df_claves.iloc[i] = [litho_cl, tema_cl, respuestas_cl]

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
    cadena = cadena.split(" ")
    # list(string) a int
    for i in range(len(cadena)):
        cadena[i] = int(cadena[i])
    return cadena

arreglo = preguntas('5 8 9 18')
mod = mod_tema('A',arreglo,df_claves)
print(df_claves)
print(mod)
