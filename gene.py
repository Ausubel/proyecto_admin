import pandas as pd
with open('identifi.sdf', "r") as archivo:
    df_identifi = pd.DataFrame(columns=['lito', 'tema', 'codigo'])
    data_identifi = archivo.readlines()
    for linea in data_identifi:
        lito = linea[:6]
        tema = linea[6]
        codigo = linea[7:].replace('\n', '')
        df_identifi = pd.concat([df_identifi, pd.DataFrame({'lito': [lito], 'tema': [tema], 'codigo': [codigo]})], ignore_index=True)

# Verifica si hay duplicados en la columna 'lito'
duplicados = df_identifi.duplicated(subset=['lito'], keep=False)

# Filtra las filas que contienen duplicados
filas_con_duplicados = df_identifi.where(duplicados).dropna()

# Muestra el resultado
print(filas_con_duplicados)


# with open('respuestas.sdf', "r") as archivo:
#     df_respuestas = pd.DataFrame(columns=['lito', 'tema', 'respuesta'])
#     data_respuestas = archivo.readlines()
#     for linea in data_respuestas:
#         lito = linea[:6]
#         tema = linea[6]
#         respuesta = linea[7:].replace('\n', '')
#         df_respuestas = pd.concat([df_respuestas, pd.DataFrame({'lito': [lito], 'tema': [tema], 'respuesta': [respuesta]})], ignore_index=True)

# print(df_identifi)
# print(df_respuestas)

# realizar un left join comparando la columna "lito"
# df_merged = pd.merge(df_identifi, df_respuestas[['lito']], on='lito', how='left', indicator=True)

# # identificar filas que no hicieron match
# df_not_matched = df_merged[df_merged['_merge'] == 'left_only'].drop('_merge', axis=1)

# # mostrar resultados
# print("Filas de df_identifi que no hacen match con df_respuestas:")
# print(df_not_matched)


# df_merged = pd.merge(df_identifi[['lito']], df_respuestas[['lito']], on='lito', how='outer', indicator=True)

# # identificar valores de "lito" que no se encontraron en cada dataframe
# df_not_in_identifi = df_merged[df_merged['_merge'] == 'right_only'].drop('_merge', axis=1)
# df_not_in_respuestas = df_merged[df_merged['_merge'] == 'left_only'].drop('_merge', axis=1)

# mostrar resultados
# print("Valores de 'lito' que no se encontraron en df_identifi:")
# print(df_not_in_identifi)
# print("Valores de 'lito' que no se encontraron en df_respuestas:")
# print(df_not_in_respuestas)





# verificar si hay valores duplicados en la columna "lito"
# duplicates = df_identifi.duplicated('lito')

# if duplicates.any():
#     print("Hay valores duplicados en la columna de identifi 'lito':")
#     print(df_identifi[duplicates])
# else:
#     print("No hay valores duplicados en la columna 'lito'.")

# # verificar si hay valores duplicados en la columna "lito"
# duplicates2 = df_respuestas.duplicated('lito')

# if duplicates2.any():
#     print("Hay valores duplicados en la columna de respuestas 'lito':")
#     print(df_respuestas[duplicates2])
# else:
#     print("No hay valores duplicados en la columna 'lito'.")