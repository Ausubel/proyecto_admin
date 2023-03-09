import pandas as pd

def qualify_normal(df_claves, df_identifi, df_respuestas):
    # Constantes para calificar
    correcta = 20
    incorrecta = 1.250
    nula = 0
    puntaje = 0

    # DataFrame con los resultados
    df_result = pd.DataFrame(columns=['lito', 'tema', 'puntaje', 'correctas', 'incorrectas', 'vacias'], index=range(len(df_respuestas)))

    for i in range(len(df_respuestas)):
        var_respuesta = df_respuestas.iloc[i, 2]
        puntaje = 0
        
        # Contadores de correctas, incorrectas, nulas
        num_cor = 0
        num_inc = 0
        num_bla = 0

        # Un bucle para comparar las respuestas con las claves
        for j in range(len(df_claves)):
            var_claves = df_claves.iloc[j, 2]
            if df_respuestas.iloc[i,1] == df_claves.iloc[j,1]:
                for k in range(len(var_respuesta)):
                    if var_claves[k] == " ":
                        puntaje += correcta
                    elif var_respuesta[k] == var_claves[k]: 
                        puntaje += correcta
                        num_cor += 1
                    elif var_respuesta[k] == " ":
                        puntaje += nula
                        num_bla += 1
                    else:
                        puntaje -= incorrecta
                        num_inc += 1
        df_result.iloc[i] = [df_respuestas.iloc[i,0], df_respuestas.iloc[i,1], puntaje, num_cor, num_inc, num_bla]

    # Se hace un merge de DataFrames -> identifi & result
    df_final = pd.merge(df_identifi, df_result, on=['lito', 'tema'])
    
    # Se cambia el orden a descendente -> puntaje
    df_final = df_final.sort_values('puntaje', ascending=False)

    # Se crean grupos de DataFrames
    groups = df_final.groupby(df_final.tema)
    df_final.to_csv('General.csv', index=False, sep=",")
    return groups