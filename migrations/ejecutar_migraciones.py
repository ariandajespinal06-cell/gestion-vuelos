import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from config.database import Database


def ejecutar():
    db = Database()
    conn = db.obtener_conexion()
    cursor = conn.cursor()

    ruta_sql = os.path.join(os.path.dirname(__file__), '001_crear_tablas.sql')
    with open(ruta_sql, 'r', encoding='utf-8') as f:
        sql = f.read()

    try:
        cursor.execute(sql)
        conn.commit()
        print(" Migración ejecutada correctamente")
    except Exception as e:
        conn.rollback()
        print(f" Error en migración: {e}")
    finally:
        cursor.close()


if __name__ == '__main__':
    ejecutar()