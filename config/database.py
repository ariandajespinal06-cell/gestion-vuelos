import psycopg2
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
                host="localhost",
                port=5432,
                dbname="db_gestionvuelos",
                user="gestion_vuelos",
                password="admin123"
            )
            self.conexion.autocommit = False
            print("Conexion exitosa")
        except Exception as e:
            print(f"Error: {e}")
            raise

    def obtener_conexion(self):
        if self.conexion.closed:
            self._conectar()
        return self.conexion

    def cerrar(self):
        if self.conexion and not self.conexion.closed:
            self.conexion.close()


# Configuracion de correo
MAIL_CONFIG = {
    'MAIL_SERVER': 'smtp.gmail.com',
    'MAIL_PORT': 587,
    'MAIL_USE_TLS': True,
    'MAIL_USERNAME': 'gestionvuelos.sistema@gmail.com',
    'MAIL_PASSWORD': 'rcrm vgcv mxbc mkbb',
    'MAIL_DEFAULT_SENDER': 'gestionvuelos.sistema@gmail.com'
}
