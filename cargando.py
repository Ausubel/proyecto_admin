import pandas as pd

def leer(ruta_archivo):
    with open(ruta_archivo, "r") as archivo:
        contenido = archivo.readlines()
        return contenido        
class Cargar():
    def __init__(self):
        pass
    def leer_claves(self,claves_lista: list) -> pd.DataFrame:
        try:
            df_claves = pd.DataFrame(columns=['lito_clave', 'tema_clave', 'solucion'])    
            data_claves = claves_lista
            for line in data_claves:
                lito = line[:6]
                tema = line[6]
                solucion = line[7:107]
                df_claves = pd.concat([df_claves, pd.DataFrame({'lito_clave': [lito], 'tema_clave': [tema], 'solucion': [solucion]})], ignore_index=True)
        except Exception as e:
            print('Hubo un error: ', e)
        return df_claves


    def leer_indentifi(self,identifi_lista: list) -> pd.DataFrame:
        try:
            df_identifi = pd.DataFrame(columns=['lito', 'tema', 'codigo'])
            data_identifi = identifi_lista
            for linea in data_identifi:
                lito = linea[:6]
                tema = linea[6]
                codigo = linea[7:13]

                df_identifi = pd.concat([df_identifi, pd.DataFrame({'lito': [lito], 'tema': [tema], 'codigo': [codigo]})], ignore_index=True)
        except Exception as e:
            print('Hubo un error: ', e)
        return df_identifi

    def leer_respuestas(self,respuestas_lista: list) -> pd.DataFrame:
        try:
            df_respuestas = pd.DataFrame(columns=['lito', 'tema', 'respuesta'])
            data_respuestas = respuestas_lista
            for linea in data_respuestas:
                lito = linea[:6]
                tema = linea[6]
                respuesta = linea[7:107]
                df_respuestas = pd.concat([df_respuestas, pd.DataFrame({'lito': [lito], 'tema': [tema], 'respuesta': [respuesta]})], ignore_index=True)
        except Exception as e:
            print('Hubo un error: ', e)
        return df_respuestas
# Evaluaciones:
# 1-Estructura: click en boton y muestre la fila que no cumple la condicion


def validando_estructura(df_claves, df_identifi, df_respuestas):
    lito_clave_esnum = pd.to_numeric(df_claves['lito_clave'], errors='coerce').notnull().all()

# 2-Validar duplicados: Devuelve la lista de los duplicados y su posicion
# 3-Validar duplicados de litos: Devuelve la lista de los duplicados y su posicion
# 4-Validar carnet postulante: Devuelve toda la info del postulante no identificado
# 5-Validar Lito no localizado
