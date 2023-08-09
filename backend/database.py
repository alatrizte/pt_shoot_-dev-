import mysql.connector
from dotenv import load_dotenv
import os

def query(sql):
    # Cargar las variables de entorno
    load_dotenv()

    # Establecer la conexión con la base de datos
    mydb = mysql.connector.connect(
    host = os.getenv("DB_HOST"),
    user = os.getenv("DB_USER"),
    password = os.getenv("DB_PASSWORD"),
    database = os.getenv("DB_NAME"),
    )

    # Crear un cursor para ejecutar la consulta
    mycursor = mydb.cursor()

    # Ejecutar la consulta
    mycursor.execute(sql)

    # Obtener los resultados de la consulta
    results = mycursor.fetchall()

    # Cerrar el cursor y la conexión
    mycursor.close()
    mydb.close()

    return results

