import pandas as pd


try:
    df_claves = pd.DataFrame(columns=['lito_clave', 'tema_clave', 'solucion'])
    with open(f'claves.sdf', 'r') as f:
        data_claves = f.readlines()

        for line in data_claves:
            lito = line[:6]
            tema = line[6]
            solucion = line[7:107]

            df_claves = pd.concat([df_claves, pd.DataFrame({'lito_clave': [
                                  lito], 'tema_clave': [tema], 'solucion': [solucion]})], ignore_index=True)
except Exception as e:
    print('Hubo un error: ', e)


try:
    df_identifi = pd.DataFrame(columns=['lito', 'tema', 'codigo'])
    with open("identifi.sdf", "r") as f:
        data_identifi = f.readlines()
        for linea in data_identifi:
            lito = linea[:6]
            tema = linea[6]
            codigo = linea[7:13]

            df_identifi = pd.concat([df_identifi, pd.DataFrame(
                {'lito': [lito], 'tema': [tema], 'codigo': [codigo]})], ignore_index=True)
except Exception as e:
    print('Hubo un error: ', e)

try:
    df_respuestas = pd.DataFrame(columns=['lito', 'tema', 'respuesta'])
    with open("respuestas.sdf", "r") as f:
        data_respuestas = f.readlines()
        for linea in data_respuestas:
            lito = linea[:6]
            tema = linea[6]
            respuesta = linea[7:107]
            df_respuestas = pd.concat([df_respuestas, pd.DataFrame(
                {'lito': [lito], 'tema': [tema], 'respuesta': [respuesta]})], ignore_index=True)
except Exception as e:
    print('Hubo un error: ', e)

# Evaluaciones:
# 1-Estructura: click en boton y muestre la fila que no cumple la condicion


def validando_estructura():
    df_claves_validas = pd.DataFrame(columns=[
                                     'lito_clave', 'tema_clave', 'solucion', 'lito', 'tema', 'codigo', 'respuesta'])

# 2-Validar duplicados: Devuelve la lista de los duplicados y su posicion
# 3-Validar duplicados de litos: Devuelve la lista de los duplicados y su posicion
# 4-Validar carnet postulante: Devuelve toda la info del postulante no identificado
# 5-Validar Lito no localizado
