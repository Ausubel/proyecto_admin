import pandas as pd
try:
    with open("identifi.sdf", "r") as archivo:
        df_identifi = pd.DataFrame(columns=['lito', 'tema', 'codigo'])
        data_identifi = archivo.readlines()
        for linea in data_identifi:
            lito = linea[:6]
            tema = linea[6]
            codigo = linea[7:13]
            df_identifi = pd.concat([df_identifi, pd.DataFrame({'lito': [lito], 'tema': [tema], 'codigo': [codigo]})], ignore_index=True)
except Exception as e:
    print('Hubo un error: ', e)

print(df_identifi)