import pandas as pd

def qualify_normal(df_claves, df_identifi, df_respuestas):    
    correcta = 20
    incorrecta = 1.250
    nula = 0
    puntaje = 0
    df_result = pd.DataFrame(columns=['lito', 'Tema', 'puntaje'], index=range(len(df_respuestas)))

    for i in range(len(df_respuestas)):
        var_respuesta = df_respuestas.iloc[i, 2]
        puntaje = 0
        for j in range(len(df_claves)):
            var_claves = df_claves.iloc[j, 2]
            if df_respuestas.iloc[i,1] == df_claves.iloc[j,1]:
                for k in range(len(var_respuesta)):
                    print("La k: "+ str(k))
                    print(var_claves)
                    print(range(len(var_respuesta)))
                    if var_respuesta[k] == var_claves[k]: 
                        puntaje += correcta
                    elif var_respuesta[k] == " ":
                        puntaje += nula
                    else:
                        puntaje -= incorrecta
        df_result.iloc[i] = [df_respuestas.iloc[i,0], df_respuestas.iloc[i,1], puntaje]

    df_final = pd.merge(df_identifi, df_result, on='lito')
    
    df_final = df_final.drop(columns=['Tema'])
    df_final = df_final.sort_values('puntaje', ascending=False)
    groups = df_final.groupby(df_final.tema)
    return groups
# import pandas as pd

# # import pandas as pd

# # def qualify_normal(df_claves, df_identifi, df_respuestas):    
# #     correcta = 20
# #     incorrecta = 1.250
# #     nula = 0
# #     puntaje = 0
# #     df_result = pd.DataFrame(columns=['lito', 'tema', 'puntaje'], index=range(len(df_respuestas)))

# #     for i in range(len(df_respuestas)):
# #         var_respuesta = df_respuestas.iloc[i, 2]
# #         puntaje = 0
# #         for j in range(len(df_claves)):
# #             var_claves = df_claves.iloc[j, 2]
# #             if df_respuestas.iloc[i,1] == df_claves.iloc[j,1]:
# #                 for k in range(len(var_respuesta)):
# #                     if var_respuesta[k] == var_claves[k]: 
# #                         puntaje += correcta
# #                     elif var_respuesta[k] == " ":
# #                         puntaje += nula
# #                     else:
# #                         puntaje -= incorrecta
# #         df_result.iloc[i] = [df_respuestas.iloc[i,0], df_respuestas.iloc[i,1], puntaje]

# #     df_final = pd.merge(df_identifi, df_result, on='lito')
    
# #     df_final = df_final.drop(columns=['tema'])
# #     df_final = df_final.sort_values('puntaje', ascending=False)
# #     groups = df_final.groupby(df_final.tema)
# #     return groups
# def qualify_normal(df_claves, df_identifi, df_respuestas):    
#     correcta = 20
#     incorrecta = 1.250
#     nula = 0
#     puntaje = 0
#     df_result = pd.DataFrame(columns=['lito', 'Tema', 'puntaje'], index=range(len(df_respuestas)))

#     for i in range(len(df_respuestas)):
#         var_respuesta = df_respuestas.iloc[i, 1]
#         puntaje = 0
#         for j in range(len(df_claves)):
#             var_claves = df_claves.iloc[j, 2]
#             if df_respuestas.iloc[i,1] == df_claves.iloc[j,1]:
#                 for k in range(len(var_respuesta)):
#                     print("La k: "+ str(k))
#                     print(var_claves)
#                     print(range(len(var_respuesta)))
#                     if var_respuesta[k] == var_claves[k]: 
#                         puntaje += correcta
#                     elif var_respuesta[k] == " ":
#                         puntaje += nula
#                     else:
#                         puntaje -= incorrecta
#         df_result.iloc[i, 0:2] = [df_respuestas.iloc[i,0], df_respuestas.iloc[i,1]]
#         df_result.iloc[i, 2] = puntaje

#     df_final = pd.merge(df_identifi, df_result, on='lito')
    
#     df_final = df_final.drop(columns=['Tema'])
#     df_final = df_final.sort_values('puntaje', ascending=False)
#     groups = df_final.groupby(df_final.tema)
#     print(df_final)
#     return groups