import bcrypt
from app.models.usuario import Usuario
from app.models.rol import Rol


class UsuarioService:

    def __init__(self):
        self._usuario_repo = Usuario()
        self._rol_repo     = Rol()

    def encriptar_password(self, password):
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

    def verificar_password(self, password, hash_guardado):
        return bcrypt.checkpw(password.encode('utf-8'), hash_guardado.encode('utf-8'))

    def crear_usuario(self, nombre, correo, password, rol_id):
        if self._usuario_repo.existe_correo(correo):
            return {'exito': False, 'id': None,
                    'error': 'El correo electrónico ya está registrado.'}

        if not self._rol_repo.rol_existe(rol_id):
            return {'exito': False, 'id': None,
                    'error': 'El rol seleccionado no existe.'}

        password_hash = self.encriptar_password(password)

        try:
            nuevo_id = self._usuario_repo.crear(nombre, correo, password_hash, int(rol_id))
            return {'exito': True, 'id': nuevo_id, 'error': None}
        except Exception as e:
            return {'exito': False, 'id': None, 'error': f'Error al crear usuario: {str(e)}'}

    def validar_rol(self, rol_id):
        return self._rol_repo.rol_existe(rol_id)

    def asignar_permisos(self, rol_id):
        return self._rol_repo.obtener_permisos_de_rol(rol_id)

    def obtener_todos(self):
        return self._usuario_repo.obtener_todos()

    def obtener_por_id(self, usuario_id):
        return self._usuario_repo.obtener_por_id(usuario_id)
    
    def login(self, correo: str, password: str) -> dict:
        """
        Verifica credenciales y retorna el usuario si son correctas.
        """
        usuario = self._usuario_repo.obtener_por_correo(correo)

        if not usuario:
            return {'exito': False, 'error': 'El correo no está registrado.', 'usuario': None}

        if not usuario['estado']:
            return {'exito': False, 'error': 'Usuario inactivo.', 'usuario': None}

        if not self.verificar_password(password, usuario['password']):
            return {'exito': False, 'error': 'Contraseña incorrecta.', 'usuario': None}

        return {'exito': True, 'error': None, 'usuario': dict(usuario)}