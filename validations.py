import pandas as pd
def duplicated_litio_solution(df_respuestas):
    duplicados = df_respuestas.duplicated(subset=['lito'], keep=False)

    print(duplicados)
    print(duplicados.any())
    if duplicados.any():
        # print("Se encontraron duplicados en la columna 'lito':\n")
        datos_duplicados = {}
        for lito, df_lito in df_respuestas[duplicados].groupby('lito'):
            if len(df_lito) > 1:
                datos_duplicados[lito] = {'tema': [], 'respuestas': [], 'indices': []}
                for idx, fila in enumerate(df_lito.itertuples(), start=1):
                    datos_duplicados[lito]['tema'].append(fila.tema)
                    datos_duplicados[lito]['respuestas'].append(fila.respuesta)
                    datos_duplicados[lito]['indices'].append(fila.Index)
                df_duplicados = pd.DataFrame({'lito': [lito]*len(df_lito), 'tema': datos_duplicados[lito]['tema'], 'respuestas': datos_duplicados[lito]['respuestas'], 'fila': datos_duplicados[lito]['indices']})
                df_duplicados += df_duplicados[['lito', 'tema', 'respuestas', 'fila']]
        return f"Se encontraron duplicados en la columna 'lito':\n{df_duplicados}"
    
    else:
        return "No se encontraron duplicados en la columna 'lito'"