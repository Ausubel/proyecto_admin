import pandas as pd

# Creamos algunos dataframes de ejemplo
df1 = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]})
df2 = pd.DataFrame({'A': [4, 5, 6], 'B': [7, 8, 9]})
df3 = pd.DataFrame({'A': [7, 8, 9], 'B': [10, 11, 12]})

# Concatenamos los dataframes en uno solo
df_concatenado = pd.concat([df1, df2, df3])

# Guardamos el dataframe concatenado en un archivo CSV
df_concatenado.to_csv('resultados.csv', index=False)