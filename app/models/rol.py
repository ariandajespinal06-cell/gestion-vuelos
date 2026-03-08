from config.database import Database
from psycopg2.extras import RealDictCursor


class Rol:

    def __init__(self):
        db = Database()
        self.conexion = db.obtener_conexion()

    def obtener_roles(self):
        sql = "SELECT id, nombre FROM roles ORDER BY nombre"
        cursor = self.conexion.cursor(cursor_factory=RealDictCursor)
        try:
            cursor.execute(sql)
            return cursor.fetchall()
        finally:
            cursor.close()

    def obtener_permisos_de_rol(self, rol_id):
        sql = """
            SELECT p.id, p.nombre
            FROM   permisos p
            JOIN   rol_permiso rp ON rp.permiso_id = p.id
            WHERE  rp.rol_id = %s
        """
        cursor = self.conexion.cursor(cursor_factory=RealDictCursor)
        try:
            cursor.execute(sql, (rol_id,))
            return cursor.fetchall()
        finally:
            cursor.close()

    def rol_existe(self, rol_id):
        sql = "SELECT id FROM roles WHERE id = %s"
        cursor = self.conexion.cursor()
        try:
            cursor.execute(sql, (rol_id,))
            return cursor.fetchone() is not None
        finally:
            cursor.close()