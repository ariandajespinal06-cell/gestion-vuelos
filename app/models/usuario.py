from config.database import Database
from psycopg2.extras import RealDictCursor


class Usuario:

    def __init__(self):
        db = Database()
        self.conexion = db.obtener_conexion()

    def crear(self, nombre, correo, password, rol_id, estado=True):
        sql = """
            INSERT INTO usuarios (nombre, correo, password, rol_id, estado)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING id
        """
        cursor = self.conexion.cursor()
        try:
            cursor.execute(sql, (nombre, correo, password, rol_id, estado))
            nuevo_id = cursor.fetchone()[0]
            self.conexion.commit()
            return nuevo_id
        except Exception as e:
            self.conexion.rollback()
            raise e
        finally:
            cursor.close()

    def obtener_todos(self):
        sql = """
            SELECT u.id, u.nombre, u.correo, u.estado, u.fecha_creacion,
                   r.nombre AS rol
            FROM   usuarios u
            JOIN   roles r ON r.id = u.rol_id
            ORDER  BY u.id
        """
        cursor = self.conexion.cursor(cursor_factory=RealDictCursor)
        try:
            cursor.execute(sql)
            return cursor.fetchall()
        finally:
            cursor.close()

    def obtener_por_id(self, usuario_id):
        sql = """
            SELECT u.id, u.nombre, u.correo, u.rol_id, u.estado,
                   r.nombre AS rol
            FROM   usuarios u
            JOIN   roles r ON r.id = u.rol_id
            WHERE  u.id = %s
        """
        cursor = self.conexion.cursor(cursor_factory=RealDictCursor)
        try:
            cursor.execute(sql, (usuario_id,))
            return cursor.fetchone()
        finally:
            cursor.close()

    def existe_correo(self, correo, excluir_id=None):
        if excluir_id:
            sql    = "SELECT id FROM usuarios WHERE correo = %s AND id != %s"
            params = (correo, excluir_id)
        else:
            sql    = "SELECT id FROM usuarios WHERE correo = %s"
            params = (correo,)
        cursor = self.conexion.cursor()
        try:
            cursor.execute(sql, params)
            return cursor.fetchone() is not None
        finally:
            cursor.close()

    def actualizar_rol(self, usuario_id, rol_id):
        sql = "UPDATE usuarios SET rol_id = %s WHERE id = %s"
        cursor = self.conexion.cursor()
        try:
            cursor.execute(sql, (rol_id, usuario_id))
            self.conexion.commit()
            return cursor.rowcount > 0
        except Exception as e:
            self.conexion.rollback()
            raise e
        finally:
            cursor.close()

    def obtener_por_correo(self, correo):
        sql = """
            SELECT u.id, u.nombre, u.correo, u.password,
                   u.rol_id, u.estado, r.nombre AS rol
            FROM   usuarios u
            JOIN   roles r ON r.id = u.rol_id
            WHERE  u.correo = %s
        """
        cursor = self.conexion.cursor(cursor_factory=RealDictCursor)
        try:
            cursor.execute(sql, (correo,))
            return cursor.fetchone()
        finally:
            cursor.close()
            
def actualizar_password(self, correo, password_hash):
        sql = "UPDATE usuarios SET password = %s WHERE correo = %s"
        cursor = self.conexion.cursor()
        try:
            cursor.execute(sql, (password_hash, correo))
            self.conexion.commit()
            return cursor.rowcount > 0
        except Exception as e:
            self.conexion.rollback()
            raise e
        finally:
            cursor.close()