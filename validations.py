import pandas as pd
import re
# Evaluaciones:
# 1-Estructura: click en boton y muestre la fila que no cumple la condicion

def estructure_solution(df_claves, df_identifi, df_respuestas, tema, patron_claves, patron_respuestas):

    men = 'VERIFICANDO CLAVES\n'

    def validar_solucion_respuesta(solucion,patron):
        if len(solucion) != 100:
            return False
        if re.match(r'^['+patron+' ]*$', str(solucion)) is None:
            return False
        return True
    # CLAVES

    # Verificando lito
    valid_lito_clave = pd.to_numeric(df_claves['lito_clave'], errors='coerce').notnull()
    valid_lito_clave_len = df_claves['lito_clave'].apply(lambda x: len(x) == 6)
    invalid_rows_lito_clave = df_claves[~(valid_lito_clave & valid_lito_clave_len)]
    if invalid_rows_lito_clave.empty:
        men += 'Hecho\n'
    else:
        men += 'Error en lito\n' + invalid_rows_lito_clave['lito_clave'].to_string(header=False) + '\n'

    # Verificando tema
    valid_tema_clave = df_claves['tema_clave'].isin([i for i in tema])
    invalid_rows_tema_clave = df_claves[~valid_tema_clave]
    if invalid_rows_tema_clave.empty:
        men += 'Hecho\n'
    else:
        men += 'Error en lito\n' + invalid_rows_tema_clave['tema_clave'].to_string(header=False) + '\n'

    # Verificando solucion

    valid_solucion_clave = df_claves['solucion'].apply(validar_solucion_respuesta, args=(patron_claves,))
    invalid_rows_solucion_clave = df_claves[~valid_solucion_clave]

    if invalid_rows_solucion_clave.empty:
        men += 'Hecho\n'
    else:
        men += 'Error en solucion\n' + invalid_rows_solucion_clave['solucion'].to_string(header=False) + '\n'
            

    men += 'VERIFICANDO IDENTIFICACIONES\n'
####################################################################
    # IDENTIFICACIONES
    # Verificando lito
    valid_lito_identifi = pd.to_numeric(df_identifi['lito'], errors='coerce').notnull()
    invalid_rows_lito_identifi = df_identifi[~valid_lito_identifi]
    if invalid_rows_lito_identifi.empty:
        men += 'Hecho\n'
    else:
        men += 'Error en lito\n' + invalid_rows_lito_identifi['lito'].to_string(header=False) + '\n'
    
    # Verificando tema
    valid_tema_identifi = df_identifi['tema'].isin([i for i in tema])
    invalid_rows_tema_identifi = df_identifi[~valid_tema_identifi]
    if invalid_rows_tema_identifi.empty:
        men += 'Hecho\n'
    else:
        men += 'Error en tema\n' + invalid_rows_tema_identifi['tema'].to_string(header=False) + '\n'
    
    # Verificando codigo
    valid_codigo_identifi = pd.to_numeric(df_identifi['codigo'], errors='coerce').notnull()
    valid_codigo_identifi_len = df_identifi['codigo'].apply(lambda x: len(x) == 8)
    invalid_rows_codigo_identifi = df_identifi[~(valid_codigo_identifi & valid_codigo_identifi_len)]
    if invalid_rows_codigo_identifi.empty:
        men += 'Hecho\n'
    else:
        men += 'Error en tema\n' + invalid_rows_codigo_identifi['codigo'].to_string(header=False) + '\n'

    men += 'VERIFICANDO RESPUESTA\n'
####################################################################
    # Verificando lito
    valid_lito_respuestas = pd.to_numeric(df_respuestas['lito'], errors='coerce').notnull()
    valid_lito_respuestas_len = df_respuestas['lito'].apply(lambda x: len(x) == 6)
    invalid_rows_lito_respuesta = df_respuestas[~(valid_lito_respuestas & valid_lito_respuestas_len)]
    if invalid_rows_lito_respuesta.empty:
        men += 'Hecho\n'
    else:
        men += 'Error en tema\n' + invalid_rows_lito_respuesta['lito'].to_string(header=False) + '\n'

    # Verificando tema
    valid_tema_respuesta = df_respuestas['tema'].isin([i for i in tema])
    invalid_rows_tema_respuestas = df_respuestas[~valid_tema_respuesta]
    if invalid_rows_tema_respuestas.empty:
        men += 'Hecho\n'
    else:
        men += 'Error en tema\n' + invalid_rows_tema_respuestas['tema'].to_string(header=False) + '\n'

    # Verificando respuesta
    valid_rows_respuestas = df_respuestas['respuesta'].apply(validar_solucion_respuesta, args=(patron_respuestas,))
    invalid_rows_respuestas = df_respuestas[~valid_rows_respuestas]

    if invalid_rows_respuestas.empty:
        men += 'Hecho\n'
    else:
        men += 'Error en respuesta\n' + invalid_rows_respuestas['respuesta'].to_string(header=False) + '\n'
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
def duplicated_litio_solution(df_identifi,df_respuestas):
    men = ""
    # cambia el indice
    df_identifi = df_identifi.reset_index(drop=True)
    df_identifi.index += 1

    # Verifica si hay duplicados en la columna 'lito'
    duplicados = df_identifi.duplicated(subset=['lito'], keep=False)

    # Filtra las filas que contienen duplicados
    filas_con_duplicados = df_identifi.where(duplicados).dropna()


    if filas_con_duplicados.empty:
        men += f"Duplicado litio identificador\nNo hay duplicados\n"
    else:
        men += f"Duplicado litio identificador\n{str(filas_con_duplicados)}\n"

    # cambia el indice
    df_respuestas = df_respuestas.reset_index(drop=True)
    df_respuestas.index += 1

    # Verifica si hay duplicados en la columna 'lito'
    duplicados = df_respuestas.duplicated(subset=['lito'], keep=False)

    # Filtra las filas que contienen duplicados
    filas_con_duplicados = df_respuestas.where(duplicados).dropna()


    if filas_con_duplicados.empty:
        men += f"Duplicado litio respuesta\nNo hay duplicados\n"
    else:
        men += f"Duplicado litio respuesta\n{str(filas_con_duplicados)}\n"

    return men
# 4-Validar carnet postulante: Devuelve toda la info del postulante no identificado

def applicant_card_solution(df_identifi, df_postulantes):
    men = ''

    df_identifi['codigo'] = df_identifi['codigo'].astype('int64')

    codigos_identifi = df_identifi['codigo'].unique()
    codigos_postulantes = df_postulantes['codigo'].unique()
    print(codigos_identifi)
    print(codigos_postulantes)
    codigos_faltantes_identifi = set(codigos_postulantes) - set(codigos_identifi)
    codigos_faltantes_postulantes = set(codigos_identifi) - set(codigos_postulantes)

    if len(codigos_faltantes_identifi) == 0:
        men += "No hay códigos faltantes en df_identifi que no estén en df_postulantes." + '\n'
    else:
        men += "Los siguientes códigos en df_postulantes no están presentes en df_identifi:" + '\n'
        men += str(df_postulantes.loc[df_postulantes['codigo'].isin(codigos_faltantes_identifi)]) + '\n'

    if len(codigos_faltantes_postulantes) == 0:
        men += "No hay códigos faltantes en df_postulantes que no estén en df_identifi." + '\n'
    else:
        men += "Los siguientes códigos en df_identifi no están presentes en df_postulantes:" + '\n'
        men += str(df_identifi.loc[df_identifi['codigo'].isin(codigos_faltantes_postulantes)]) + '\n'
    return men

# 5-Validar Lito no localizado o tema inconsistente
def lito_not_located(df_identifi, df_respuestas):
    # Unir los dataframes y filtrar las filas no localizadas
    merged = pd.merge(df_identifi, df_respuestas, on=['lito', 'tema'], how='outer', indicator=True)
    no_localizados = merged.query("_merge == 'right_only'").loc[:, ['lito']]
    men = ''
    # Mostrar los resultados
    if no_localizados.empty:
        men += "Todos han sido localizados de identificador a respuesta\n"
    else:
        men += f"DataFrame no localizado de identificador a respuesta\n{pd.DataFrame({'lito': no_localizados['lito']})}\n"

    # Unir los dataframes y filtrar las filas no localizadas
    merged = pd.merge(df_respuestas, df_identifi, on=['lito', 'tema'], how='outer', indicator=True)
    no_localizados = merged.query("_merge == 'right_only'").loc[:, ['lito']]

    # Mostrar los resultados
    if no_localizados.empty:
        men += "Todos han sido localizados de respuestas a identificador\n"
    else:
        men += f"DataFrame no localizado de respuestas a identificador\n{pd.DataFrame({'lito': no_localizados['lito']})}\n"
    return men