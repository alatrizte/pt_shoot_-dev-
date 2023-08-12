import mysql.connector
from dotenv import load_dotenv
import os

def conn():
    # Cargar las variables de entorno
    load_dotenv()

    # Establecer la conexión con la base de datos
    mydb = mysql.connector.connect(
    host = os.getenv("DB_HOST"),
    user = os.getenv("DB_USER"),
    password = os.getenv("DB_PASSWORD"),
    database = os.getenv("DB_NAME"),
    )

    return mydb

def query(sql, values):
    
    conn_db = conn()
    # Crear un cursor para ejecutar la consulta
    mycursor = conn_db.cursor()

    # Ejecutar la consulta
    mycursor.execute(sql, values)

    # Obtener los resultados de la consulta
    results = mycursor.fetchall()

    # Cerrar el cursor y la conexión
    mycursor.close()
    conn_db.close()

    return results

def insert(sql, values):
    conn_db = conn()
    print (values)
    # Crear un cursor para ejecutar la consulta
    mycursor = conn_db.cursor()
    try:
        # Ejecutar la consulta
        mycursor.execute(sql, values)
        conn_db.commit()
        # Cerrar el cursor y la conexión
        mycursor.close()
        conn_db.close()
        return True
    except:
        return False

