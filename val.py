import pandas as pd

try:
    with open('id.sdf', "r") as archivo:
        df_identifi = pd.DataFrame(columns=['lito', 'tema', 'codigo'])
        data_identifi = archivo.readlines()
        for linea in data_identifi:
            lito = linea[:6]
            tema = linea[6]
            codigo = linea[7:13]
            df_identifi = pd.concat([df_identifi, pd.DataFrame({'lito': [lito], 'tema': [tema], 'codigo': [codigo]})], ignore_index=True)
    # print(df_identifi)
except Exception as e:
    print('Hubo un error: ', e)

try:
    with open("res.sdf", "r") as archivo:
        df_respuestas = pd.DataFrame(columns=['lito', 'tema', 'respuesta'])
        data_respuestas = archivo.readlines()
        for linea in data_respuestas:
            lito = linea[:6]
            tema = linea[6]
            respuesta = linea[7:107]
            df_respuestas = pd.concat([df_respuestas, pd.DataFrame({'lito': [lito], 'tema': [tema], 'respuesta': [respuesta]})], ignore_index=True)
    # print(df_respuestas)
except Exception as e:
    print('Hubo un error: ', e)

# Validacion match

# # Combinar los dataframes por la columna "lito"
# combinados = pd.merge(df_identifi, df_respuestas, on='lito', how='outer')

# # Encontrar los lítos sin pareja
# sin_pareja = combinados[(combinados['codigo'].isnull()) | (combinados['respuesta'].isnull())]['lito'].tolist()

# # Imprimir la lista de lítos sin pareja
# print(sin_pareja)


## PPRIMERO VALIDAR ESTRUCTURA
##
# Combinar los dataframes por la columna "lito"
combinados = pd.merge(df_identifi, df_respuestas, on='lito', how='outer')

# Encontrar los lítos sin pareja
sin_pareja = []

for i, row in combinados.iterrows():
    if pd.isna(row['codigo']):
        sin_pareja.append(('respuestas', i, row['lito']))
    elif pd.isna(row['respuesta']):
        sin_pareja.append(('identificador', i, row['lito']))

# Imprimir la lista de lítos sin pareja con su número de fila y nombre de dataframe
for nombre_df, num_fila, lito in sin_pareja:
    if(num_fila>=df_respuestas.shape[0]):
        print(f"Lito {lito} sin pareja ubicado en {nombre_df}.sdf en la fila {num_fila+1-5}")
    else:
        print(f"Lito {lito} sin pareja ubicado en {nombre_df}.sdf en la fila {num_fila+1}")
