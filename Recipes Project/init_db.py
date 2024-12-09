from __init__ import db, app
from models import Usuario, Receta, Ingrediente, RecetaIngrediente, FotoReceta
import mysql.connector
from config import Config
import os
from dotenv import load_dotenv

load_dotenv()

def init_db():
    # Conectar a MySQL sin seleccionar una base de datos
    conn = mysql.connector.connect(
        host=os.getenv('MYSQL_HOST'),
        user=os.getenv('MYSQL_USER'),
        password=os.getenv('MYSQL_PASSWORD')
    )
    cursor = conn.cursor()

    # Recrear la base de datos
    cursor.execute("DROP DATABASE IF EXISTS alimentacion")
    cursor.execute("CREATE DATABASE alimentacion")
    cursor.execute("USE alimentacion")
    
    # Crear la tabla usuario con LONGTEXT para password_hash
    cursor.execute("""
    CREATE TABLE usuario (
        id INT AUTO_INCREMENT PRIMARY KEY,
        username VARCHAR(50) UNIQUE NOT NULL,
        email VARCHAR(120) UNIQUE NOT NULL,
        password_hash LONGTEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    
    # Cerrar la conexión inicial
    cursor.close()
    conn.close()

    # Ahora usar SQLAlchemy para crear las tablas restantes
    with app.app_context():
        db.create_all()
        print("Base de datos inicializada correctamente")

if __name__ == "__main__":
    init_db() 