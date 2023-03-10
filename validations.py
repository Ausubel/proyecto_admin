import pandas as pd
import re
# Evaluaciones:
# 1-Estructura: click en boton y muestre la fila que no cumple la condicion

def estructure_solution(df_claves, df_identifi, df_respuestas, tema, patron_claves, patron_respuestas):
    # Cambiando indice
    df_claves = df_claves.reset_index(drop=True)
    df_claves.index += 1

    df_identifi = df_identifi.reset_index(drop=True)
    df_identifi.index += 1

    df_respuestas = df_respuestas.reset_index(drop=True)
    df_respuestas.index += 1


    men = 'Verificando claves'
    men += '\n'

    def validar_solucion_respuesta(solucion,patron):
        if len(solucion) != 100:
            return False
        if re.match(r'^['+patron+' ]*$', str(solucion)) is None:
            return False
        return True
    
    # Verificando lito
    lito_clave_esnum = pd.to_numeric(df_claves['lito_clave'], errors='coerce').notnull()
    invalid_rows = df_claves[~lito_clave_esnum]
    if invalid_rows.empty:
        men += 'Hecho\n'
    else:
        men += 'Error en lito\n' + invalid_rows['lito_clave'].to_string(header=False) + '\n'

    # Verificando tema
    valid_tema = df_identifi['tema'].isin([i for i in tema])
    invalid_rows = df_identifi[~valid_tema]
    if invalid_rows.empty:
        men += 'Hecho\n'
    else:
        men += 'Error en lito\n' + invalid_rows['tema'].to_string(header=False) + '\n'

    # Verificando solucion

    valid_rows = df_claves['solucion'].apply(validar_solucion_respuesta, args=(patron_claves,))
    invalid_rows = df_claves[~valid_rows]

    if invalid_rows.empty:
        men += 'Hecho\n'
    else:
        men += 'Error en solucion\n' + invalid_rows['solucion'].to_string(header=False) + '\n'
            

    men += 'Verificando identificaciones'
    men += '\n'

    # Verificando identificaciones
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
    # invalid_codigo_identifi = df_identifi[~valid_codigo_identifi]
    # invalid_codigo_identifi_len  = df_identifi[~valid_codigo_identifi_len]
    invalid_rows_codigo_identifi = df_identifi[~(valid_codigo_identifi & valid_codigo_identifi_len)]
    if invalid_rows_codigo_identifi.empty:
        men += 'Hecho\n'
    else:
        men += 'Error en tema\n' + invalid_rows_codigo_identifi['codigo'].to_string(header=False) + '\n'

    men += 'Verificando Respuestas'
    men += '\n'

    # Verificando lito
    valid_lito_respuestas = pd.to_numeric(df_respuestas['lito'], errors='coerce').notnull()
    valid_codigo_identifi_len = df_identifi['lito'].apply(lambda x: len(x) == 6)
    invalid_lito_respuesta = df_respuestas[~valid_lito_respuestas]
    if invalid_lito_respuesta.empty:
        men += 'Hecho\n'
    else:
        men += 'Error en tema\n' + invalid_lito_respuesta['lito'].to_string(header=False) + '\n'

    # Verificando tema
    valid_tema_respuestas = df_respuestas['tema'].isin([i for i in tema])
    invalid_rows_tema_respuestas = df_respuestas[~valid_tema_respuestas]
    if invalid_rows_codigo_identifi.empty:
        men += 'Hecho\n'
    else:
        men += 'Error en tema\n' + invalid_rows_codigo_identifi['tema'].to_string(header=False) + '\n'

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
    df_identifi = df_identifi.reset_index(drop=True)
    df_identifi.index += 1
    df_postulantes = df_postulantes.reset_index(drop=True)
    df_postulantes.index += 1

    df_identifi['codigo'] = df_identifi['codigo'].astype('int64')

    codigos_identifi = df_identifi['codigo'].unique()
    codigos_postulantes = df_postulantes['codigo'].unique()

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

# 5-Validar Lito no localizado
def lito_not_located(df_identifi, df_respuestas):
    # Unir los dataframes y filtrar las filas no localizadas
    merged = pd.merge(df_identifi, df_respuestas, on=['lito', 'tema'], how='outer', indicator=True)
    no_localizados = merged.query("_merge == 'right_only'").loc[:, ['lito']]
    men = ''
    # Mostrar los resultados
    if no_localizados.empty:
        men += "Todos han sido localizados de identificador a respuesta"
    else:
        men += f"DataFrame no localizado de identificador a respuesta\n{pd.DataFrame({'lito': no_localizados['lito']})}"

    # Unir los dataframes y filtrar las filas no localizadas
    merged = pd.merge(df_respuestas, df_identifi, on=['lito', 'tema'], how='outer', indicator=True)
    no_localizados = merged.query("_merge == 'right_only'").loc[:, ['lito']]

    # Mostrar los resultados
    if no_localizados.empty:
        men += "Todos han sido localizados de respuestas a identificador"
    else:
        men += f"DataFrame no localizado de respuestas a identificador\n{pd.DataFrame({'lito': no_localizados['lito']})}"
    return men