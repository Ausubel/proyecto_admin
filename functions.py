from main import ruta_archivo
def read_file():
    with open(ruta_archivo, "r") as archivo:
        # Realizar operaciones en el archivo
        contenido = archivo.read()
        print(contenido)
