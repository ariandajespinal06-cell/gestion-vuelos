import psycopg2
import os
from psycopg2.extras import RealDictCursor

class Database:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._conectar()
        return cls._instance

    def _conectar(self):
        try:
            self.conexion = psycopg2.connect(
                host=os.environ.get("PGHOST"),
                port=os.environ.get("PGPORT", 5432),
                dbname=os.environ.get("PGDATABASE"),
                user=os.environ.get("PGUSER"),
                password=os.environ.get("PGPASSWORD")
            )
            self.conexion.autocommit = False
            print('Conexion exitosa')
        except Exception as e:
            print(f'Error: {e}')
            raise

    def obtener_conexion(self):
        if self.conexion.closed:
            self._conectar()
        return self.conexion

    def cerrar(self):
        if self.conexion and not self.conexion.closed:
            self.conexion.close()
