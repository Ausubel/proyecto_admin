# Evaluaciones:
# 1-Estructura: click en boton y muestre la fila que no cumple la condicion


def validando_estructura(df_claves, df_identifi, df_respuestas):
    lito_clave_esnum = pd.to_numeric(df_claves['lito_clave'], errors='coerce').notnull().all()

# 2-Validar duplicados: Devuelve la lista de los duplicados y su posicion
# 3-Validar duplicados de litos: Devuelve la lista de los duplicados y su posicion
# 4-Validar carnet postulante: Devuelve toda la info del postulante no identificado
# 5-Validar Lito no localizado