import pandas as pd

# Evaluaciones:
# 1-Estructura: click en boton y muestre la fila que no cumple la condicion

def estructure_solution(df_claves, df_identifi, df_respuestas, tema):
    men = 'Verificando claves'
    men += '\n'

    # Verificando lito
    lito_clave_esnum = pd.to_numeric(df_claves['lito_clave'], errors='coerce').notnull()
    invalid_rows = df_claves[~lito_clave_esnum]
    if invalid_rows.empty:
        men += 'Hecho'
        men += '\n'
    else:
        men += 'Error en lito'
        men += str(invalid_rows)
        men += '\n'

    # Verificando tema
    valid_tema = df_claves['tema_clave'].isin([i for i in tema])
    invalid_rows = df_claves[~valid_tema]
    if invalid_rows.empty:
        men += 'Hecho'
        men += '\n'
    else:
        men += 'Error en tema'
        men += str(invalid_rows)

    # Verificando solucion
    valid_codigo= df_claves['solucion'].apply(lambda x: len(x) == 100 and x[99] != "\n")
    invalid_rows = df_claves[~valid_codigo]
    invalid_len_rows = df_claves.loc[~valid_codigo, ['solucion']]

    if invalid_rows.empty and invalid_len_rows.empty:
        men += 'Hecho'
        men += '\n'
    else:
        men += 'Error en solucion'
        men += '\n'
        if not invalid_rows.empty:
            men += str(invalid_rows)
        if not invalid_len_rows.empty:
            men += str(invalid_len_rows)
            men += '\n'
    
    men += 'Verificando identificaciones'
    men += '\n'

    # Verificando lito
    valid_lito_esnum = pd.to_numeric(df_identifi['lito'], errors='coerce').notnull()
    invalid_rows = df_identifi[~valid_lito_esnum]
    if invalid_rows.empty:
        men += 'Hecho'
        men += '\n'
    else:
        men += 'Error en lito'
        men += str(invalid_rows)
        men += '\n'
    
    # Verificando tema
    valid_tema = df_identifi['tema'].isin([i for i in tema])
    invalid_rows = df_identifi[~valid_tema]
    if invalid_rows.empty:
        men += 'Hecho'
        men += '\n'
    else:
        men += 'Error en tema'
        men += '\n'
        men += str(invalid_rows)
        men += '\n'
    
    # Verificando codigo
    valid_codigo= pd.to_numeric(df_identifi['codigo'], errors='coerce').notnull()
    valid_codigo_len = df_identifi['codigo'].apply(lambda x: len(x) == 6 and x[5] != "\n")
    invalid_rows = df_identifi[~valid_codigo]
    invalid_len_and_num_rows = df_identifi[~(valid_codigo & valid_codigo_len)]
    if invalid_rows.empty and invalid_len_and_num_rows.empty:
        men += 'Hecho'
        men += '\n'
    else:
        if not invalid_rows.empty:
            men += 'Filas con códigos inválidos:'
            men += '\n'
            men += str(invalid_rows)
            men += '\n'
        if not invalid_len_and_num_rows.empty:
            men += 'Filas con longitud de código inválida:'
            men += '\n'
            men += str(invalid_len_and_num_rows)
            men += '\n'

    men += 'Verificando Respuestas'
    men += '\n'

    # Verificando lito
    valid_lito= pd.to_numeric(df_respuestas['lito'], errors='coerce').notnull()
    invalid_rows = df_respuestas[~valid_lito]
    if invalid_rows.empty:
        men += 'Hecho'
        men += '\n'
    else:
        men += 'Error en lito'
        men += '\n'
        men += str(invalid_rows)
        men += '\n'

    # Verificando tema
    valid_tema = df_respuestas['tema'].isin([i for i in tema])
    invalid_rows = df_respuestas[~valid_tema]
    if invalid_rows.empty:
        men += 'Hecho'
        men += '\n'
    else:
        men += 'Error en tema'
        men += '\n'
        men += str(invalid_rows)
        men += '\n'

    # Verificando respuesta
    valid_codigo= df_respuestas['respuesta'].apply(lambda x: len(x) == 100 and x[99] != "\n")
    invalid_rows = df_respuestas[~valid_codigo]
    invalid_len_rows = df_respuestas.loc[~valid_codigo, ['respuesta']]
    if invalid_rows.empty and invalid_len_rows.empty:
        men += 'Hecho'
        men += '\n'
    else:
        men += 'Error en respuesta'
        if not invalid_rows.empty:
            men += str(invalid_rows)
            men += '\n'
        if not invalid_len_rows.empty:
            men += str(invalid_len_rows)
            men += '\n'
    return men

# 2-Validar duplicados: Devuelve la lista de los duplicados y su posicion
def duplicated_code_solution(df_identifi):
    res = ""
    duplicados = df_identifi.duplicated(subset=['codigo'], keep=False)
    if duplicados.any():
        res += "Se encontraron codigos duplicados:\n\n"
        datos_duplicados = {}
        for codigo, df_codigo in df_identifi[duplicados].groupby('codigo'):
            if len(df_codigo) > 1:
                datos_duplicados[codigo] = {'lito': [], 'tema': [], 'indices': []}
                for idx, fila in enumerate(df_codigo.itertuples(), start=1):
                    datos_duplicados[codigo]['lito'].append(fila.lito)
                    datos_duplicados[codigo]['tema'].append(fila.tema)
                    datos_duplicados[codigo]['indices'].append(fila.Index)
                df_duplicados = pd.DataFrame({'lito': datos_duplicados[codigo]['lito'], 'tema': datos_duplicados[codigo]['tema'], 'codigo': [codigo]*len(df_codigo), 'fila': datos_duplicados[codigo]['indices']})
                df_duplicados = df_duplicados[['lito', 'tema', 'codigo', 'fila']]
                res += f"{str(df_duplicados)}\n"
    else:
        res += "No se encontraron duplicados en la columna 'codigo'"
    return res
# 3-Validar duplicados de litos: Devuelve la lista de los duplicados y su posicion
def duplicated_litio_solution(df_respuestas):
    duplicados = df_respuestas.duplicated(subset=['lito'], keep=False)
    # print(duplicados)
    # print(duplicados.any())
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
# 4-Validar carnet postulante: Devuelve toda la info del postulante no identificado

def applicant_card_solution(df_respuestas):
    pass

# 5-Validar Lito no localizado

def litos_solution(df_identifi, df_respuestas):
    # crea una serie booleana que indica si cada valor de la primera columna de df_identifi está en la primera columna de df_respuestas
    identifi_in_respuestas = df_identifi.iloc[:, 0].isin(df_respuestas.iloc[:, 0])
    # crea una lista con las filas de df_identifi que no tienen coincidencias
    exce = [f'{i + 1}: No se encontro {df_identifi.iloc[i, 2]}.\n' for i, val in enumerate(identifi_in_respuestas) if not val]
    # une los elementos de la lista en una cadena de texto
    exce_str = ''.join(exce)
    if exce_str!='':
        return exce_str
    else:
        return 'Todos los litos estan localizados'