
import pandas as pd

# Evaluaciones:
# 1-Estructura: click en boton y muestre la fila que no cumple la condicion

def validar_estructura(DF_CLAVES, DF_IDENTIFI, DF_RESPUESTAS, TEMA):
    men = ''
    if 'lito_clave' not in DF_CLAVES.columns or 'lito_id' not in DF_IDENTIFI.columns or 'respuesta' not in DF_RESPUESTAS.columns:
        return "Error: alguna(s) de las columnas necesarias no están presentes en los DataFrames."

    # Claves

    # Verificando lito
    lito_clave_esnum = pd.to_numeric(DF_CLAVES['lito_clave'], errors='coerce').notnull()
    invalid_rows = DF_CLAVES[~lito_clave_esnum]
    if invalid_rows.empty:
        men += 'No hay datos invalidos'
    else:
        men += invalid_rows

    # Verificando tema
    valid_tema = DF_CLAVES['tema_clave'].isin([i for i in TEMA])
    invalid_rows = DF_CLAVES[~valid_tema]
    if invalid_rows.empty:
        men += 'No hay datos invalidos'
    else:
        men += invalid_rows

    # Verificando solucion
    valid_codigo= DF_CLAVES['solucion'].apply(lambda x: len(x) == 100 and x[99] != "\n")
    invalid_rows = DF_CLAVES[~valid_codigo]
    invalid_len_rows = DF_CLAVES.loc[~valid_codigo, ['solucion']]

    if invalid_rows.empty and invalid_len_rows.empty:
        men += 'No hay datos invalidos'
    else:
        if not invalid_rows.empty:
            men += invalid_rows
        if not invalid_len_rows.empty:
            men += invalid_len_rows
    
    # Identificaciones

    # Verificando lito
    valid_lito_esnum = pd.to_numeric(DF_IDENTIFI['lito'], errors='coerce').notnull()
    invalid_rows = DF_IDENTIFI[~valid_lito_esnum]
    if invalid_rows.empty:
        men += 'No hay datos invalido'
    else:
        men += invalid_rows
    
    # Verificando tema
    valid_tema = DF_IDENTIFI['tema'].isin([i for i in 'ABCDPQRS'])
    invalid_rows = DF_IDENTIFI[~valid_tema]
    if invalid_rows.empty:
        men += 'No hay datos invalido'
    else:
        men += invalid_rows
    
    # Verificando codigo
    valid_codigo= pd.to_numeric(DF_IDENTIFI['codigo'], errors='coerce').notnull()
    valid_codigo_len = DF_IDENTIFI['codigo'].apply(lambda x: len(x) == 6 and x[5] != "\n")
    invalid_rows = DF_IDENTIFI[~valid_codigo]
    invalid_len_and_num_rows = DF_IDENTIFI[~(valid_codigo & valid_codigo_len)]
    if invalid_rows.empty and invalid_len_and_num_rows.empty:
        men += 'No hay datos invalido'
    else:
        if not invalid_rows.empty:
            men += 'Filas con códigos inválidos:'
            men += invalid_rows
        if not invalid_len_and_num_rows.empty:
            men += 'Filas con longitud de código inválida:'
            men += invalid_len_and_num_rows

    # Respuestas

    # Verificando lito
    valid_lito= pd.to_numeric(DF_RESPUESTAS['lito'], errors='coerce').notnull()
    invalid_rows = DF_RESPUESTAS[~valid_lito]
    if invalid_rows.empty:
        men += 'No hay datos invalido'
    else:
        men += invalid_rows

    # Verificando tema
    valid_tema = DF_RESPUESTAS['tema'].isin([i for i in TEMA])
    invalid_rows = DF_RESPUESTAS[~valid_tema]
    if invalid_rows.empty:
        men += 'No hay datos invalido'
    else:
        men += invalid_rows

    # Verificando respuesta
    valid_codigo= DF_RESPUESTAS['respuesta'].apply(lambda x: len(x) == 100 and x[99] != "\n")
    invalid_rows = DF_RESPUESTAS[~valid_codigo]
    invalid_len_rows = DF_RESPUESTAS.loc[~valid_codigo, ['respuesta']]
    if invalid_rows.empty and invalid_len_rows.empty:
        men += 'No hay datos invalido'
    else:
        if not invalid_rows.empty:
            men += invalid_rows
        if not invalid_len_rows.empty:
            men += invalid_len_rows
    return men

# 2-Validar duplicados: Devuelve la lista de los duplicados y su posicion
def validar_duplicados(DF_IDENTIFI):
    men = ''
    duplicados = DF_IDENTIFI.duplicated(subset=['codigo'], keep=False)
    if duplicados.any():
        men += "Se encontraron duplicados en la columna 'codigo':\n"
        datos_duplicados = {}
        for codigo, df_codigo in DF_IDENTIFI[duplicados].groupby('codigo'):
            if len(df_codigo) > 1:
                datos_duplicados[codigo] = {'lito': [], 'tema': [], 'indices': []}
                for idx, fila in enumerate(df_codigo.itertuples(), start=1):
                    datos_duplicados[codigo]['lito'].append(fila.lito)
                    datos_duplicados[codigo]['tema'].append(fila.tema)
                    datos_duplicados[codigo]['indices'].append(fila.Index)
                df_duplicados = pd.DataFrame({'lito': datos_duplicados[codigo]['lito'], 'tema': datos_duplicados[codigo]['tema'], 'codigo': [codigo]*len(df_codigo), 'fila': datos_duplicados[codigo]['indices']})
                df_duplicados = df_duplicados[['lito', 'tema', 'codigo', 'fila']]
                men += df_duplicados
    else:
        men += "No se encontraron duplicados en la columna 'codigo'"
    return men
# 3-Validar duplicados de litos: Devuelve la lista de los duplicados y su posicion
def validar_duplicados_lito(DF_IDENTIFI):
    men = ''
    duplicados = DF_IDENTIFI.duplicated(subset=['lito'], keep=False)
    if duplicados.any():
        men += "Se encontraron duplicados en la columna 'lito':\n"
        datos_duplicados = {}
        for lito, df_lito in DF_IDENTIFI[duplicados].groupby('lito'):
            if len(df_lito) > 1:
                datos_duplicados[lito] = {'codigo': [], 'tema': [], 'indices': []}
                for idx, fila in enumerate(df_lito.itertuples(), start=1):
                    datos_duplicados[lito]['codigo'].append(fila.codigo)
                    datos_duplicados[lito]['tema'].append(fila.tema)
                    datos_duplicados[lito]['indices'].append(fila.Index)
                df_duplicados = pd.DataFrame({'codigo': datos_duplicados[lito]['codigo'], 'tema': datos_duplicados[lito]['tema'], 'lito': [lito]*len(df_lito), 'fila': datos_duplicados[lito]['indices']})
                df_duplicados = df_duplicados[['lito', 'tema', 'codigo', 'fila']]
                print(df_duplicados)
    else:
        men += "No se encontraron duplicados en la columna 'lito'"
    return men
# 4-Validar carnet postulante: Devuelve toda la info del postulante no identificado

def validar_carnet_postulante(DF_RESPUESTAS):
    men = ''
    duplicados = DF_RESPUESTAS.duplicated(subset=['lito'], keep=False)
    if duplicados.any():
        print("Se encontraron duplicados en la columna 'lito':\n")
        datos_duplicados = {}
        for lito, df_lito in DF_RESPUESTAS[duplicados].groupby('lito'):
            if len(df_lito) > 1:
                datos_duplicados[lito] = {'tema': [], 'respuestas': [], 'indices': []}
                for idx, fila in enumerate(df_lito.itertuples(), start=1):
                    datos_duplicados[lito]['tema'].append(fila.tema)
                    datos_duplicados[lito]['respuestas'].append(fila.respuesta)
                    datos_duplicados[lito]['indices'].append(fila.Index)
                df_duplicados = pd.DataFrame({'lito': [lito]*len(df_lito), 'tema': datos_duplicados[lito]['tema'], 'respuestas': datos_duplicados[lito]['respuestas'], 'fila': datos_duplicados[lito]['indices']})
                df_duplicados = df_duplicados[['lito', 'tema', 'respuestas', 'fila']]
                men += df_duplicados
    else:
        men += "No se encontraron duplicados en la columna 'lito'"
    return men
# 5-Validar Lito no localizado