# import random

# letras = ['F','G','H','I','J','K','L','M','N','O','P','R','S','T','U','V','W','X','Y','Z']

# filas = []
# while len(filas) < 1094:
#     numeros = random.sample(range(100000, 999999), 1)
#     letra = random.choice(letras)
#     fila = f"{numeros[0]}{letra}"
#     if fila not in filas:
#         filas.append(fila)

# with open('prueba.txt', 'w') as archivo:

#     # Convertir la lista a una cadena de texto
#     contenido = '\n'.join(filas)

#     # Escribir el contenido en el archivo
#     archivo.write(contenido)
##############################

# # Leer el contenido del primer archivo
# with open('prueba.txt', 'r') as archivo1:
#     contenido1 = archivo1.readlines()

# # Leer el contenido del segundo archivo
# with open('codigos.txt', 'r') as archivo2:
#     contenido2 = archivo2.readlines()

# # Unir las líneas de ambos archivos
# filas = []
# for i in range(len(contenido1)):
#     fila = contenido1[i].strip() + contenido2[i].strip() + '\n'
#     filas.append(fila)

# # Escribir el contenido en un nuevo archivo
# with open('nuevo_identificador.txt', 'w') as archivo_nuevo:
#     archivo_nuevo.writelines(filas)


import random

clave = "ABCDE *"

# Leer el contenido del archivo
with open('prueba.txt', 'r') as archivo:
    contenido = archivo.readlines()

# Recorrer cada fila del archivo y agregar letras al azar
filas = []
for fila in contenido:
    fila = fila.strip()
    letras_aleatorias = ''.join(random.sample(clave, 10))
    fila_nueva = fila + '' + letras_aleatorias
    filas.append(fila_nueva + '\n')

# Escribir las filas con las letras aleatorias en un nuevo archivo
with open('nuevo_respuesta.txt', 'w') as archivo_nuevo:
    archivo_nuevo.writelines(filas)