import pandas as pd

def leer(ruta_archivo):
    with open(ruta_archivo, "r") as archivo:
        contenido = archivo.readlines()
        return contenido
class Cargar():
    def __init__(self):
        pass
    def leer_claves(self,ruta_archivo: list) -> pd.DataFrame:
        try:
            with open(ruta_archivo, "r") as archivo:
                df_claves = pd.DataFrame(columns=['lito_clave', 'tema_clave', 'solucion'])    
                data_claves = archivo.readlines()
                for line in data_claves:
                    lito = line[:6]
                    tema = line[6]
                    solucion = line[8:].replace('\n', '')
                    df_claves = pd.concat([df_claves, pd.DataFrame({'lito_clave': [lito], 'tema_clave': [tema], 'solucion': [solucion]})], ignore_index=True)            
                archivo.close()
            return df_claves
        except Exception as e:
            print('Hubo un error: ', e)
        


    def leer_indentifi(self,ruta_archivo: list) -> pd.DataFrame:
        try:
            with open(ruta_archivo, "r") as archivo:
                df_identifi = pd.DataFrame(columns=['lito', 'tema', 'codigo'])
                data_identifi = archivo.readlines()
                for linea in data_identifi:
                    lito = linea[:6]
                    tema = linea[6]
                    codigo = linea[7:].replace('\n', '')
                    df_identifi = pd.concat([df_identifi, pd.DataFrame({'lito': [lito], 'tema': [tema], 'codigo': [codigo]})], ignore_index=True)
        except Exception as e:
            print('Hubo un error: ', e)
        return df_identifi

    def leer_respuestas(self,ruta_archivo: list) -> pd.DataFrame:
        try:
            with open(ruta_archivo, "r") as archivo:
                df_respuestas = pd.DataFrame(columns=['lito', 'tema', 'respuesta'])
                data_respuestas = archivo.readlines()
                for linea in data_respuestas:
                    lito = linea[:6]
                    tema = linea[6]
                    respuesta = linea[8:].replace('\n', '')
                    df_respuestas = pd.concat([df_respuestas, pd.DataFrame({'lito': [lito], 'tema': [tema], 'respuesta': [respuesta]})], ignore_index=True)
        except Exception as e:
            print('Hubo un error: ', e)
        return df_respuestas
