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

MAIL_CONFIG = {
    'MAIL_SERVER': 'smtp.gmail.com',
    'MAIL_PORT': 587,
    'MAIL_USE_TLS': True,
    'MAIL_USERNAME': os.environ.get('MAIL_USERNAME', ''),
    'MAIL_PASSWORD': os.environ.get('MAIL_PASSWORD', ''),
    'MAIL_DEFAULT_SENDER': os.environ.get('MAIL_USERNAME', '')
}
