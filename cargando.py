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
                    solucion = line[7:107]
                    df_claves = pd.concat([df_claves, pd.DataFrame({'lito_clave': [lito], 'tema_clave': [tema], 'solucion': [solucion]})], ignore_index=True)            
                archivo.close()
            return df_claves
        except Exception as e:
            print('Hubo un error: ', e)
        


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
