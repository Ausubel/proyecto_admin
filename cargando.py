import mysql.connector

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="intelectus",
    database="db_admision"
)

cursor = db.cursor()

with open('claves.sdf', 'r') as f:
    lines = f.readlines()
    for line in lines:
        lito = line[:6]
        tema = line[6]
        solucion = line[7:]
    
        sql = "INSERT INTO Claves (Lito, Tema, Solución) VALUES (%s, %s, %s)"
        values = (lito, tema, solucion)
        cursor.execute(sql, values)

db.commit()

cursor.close()
db.close()