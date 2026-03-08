from app.controllers.usuario_service import UsuarioService
from app.controllers.rol_service import RolService
from app.helpers.validaciones import Validaciones


class UsuarioFacade:
    def __init__(self):
        self._usuario_service = UsuarioService()
        self._rol_service     = RolService()

    def crear_usuario(self, datos):
        errores = Validaciones.validar_usuario(datos)
        if errores:
            return {'exito': False, 'errores': errores, 'id': None, 'permisos': []}

        resultado = self._usuario_service.crear_usuario(
            nombre=datos['nombre'].strip(),
            correo=datos['correo'].strip().lower(),
            password=datos['password'],
            rol_id=int(datos['rol_id'])
        )

        if not resultado['exito']:
            return {'exito': False, 'errores': [resultado['error']],
                    'id': None, 'permisos': []}

        permisos = self._usuario_service.asignar_permisos(int(datos['rol_id']))

        return {
            'exito': True,
            'errores': [],
            'id': resultado['id'],
            'permisos': [p['nombre'] for p in permisos]
        }

    def obtener_roles(self):
        return self._rol_service.obtener_roles()

    def listar_usuarios(self):
        return self._usuario_service.obtener_todos()

    def editar_rol_usuario(self, usuario_id, rol_id):
        errores = Validaciones.validar_rol({'rol_id': rol_id})
        if errores:
            return {'exito': False, 'errores': errores}

        from app.models.usuario import Usuario
        repo = Usuario()
        try:
            ok = repo.actualizar_rol(usuario_id, int(rol_id))
            if ok:
                return {'exito': True, 'errores': []}
            return {'exito': False, 'errores': ['Usuario no encontrado.']}
        except Exception as e:
            return {'exito': False, 'errores': [str(e)]}

    def obtener_usuario(self, usuario_id):
        return self._usuario_service.obtener_por_id(usuario_id)
    
    def login(self, correo: str, password: str) -> dict:
        """
        Facade para el login.
        Verifica credenciales y retorna rol del usuario.
        """
        if not correo or not password:
            return {'exito': False, 'error': 'Correo y contraseña son obligatorios.', 'usuario': None}

        resultado = self._usuario_service.login(correo, password)

        if not resultado['exito']:
            return resultado

        usuario = resultado['usuario']

        # Obtener permisos del rol
        permisos = self._usuario_service.asignar_permisos(usuario['rol_id'])
        usuario['permisos'] = [p['nombre'] for p in permisos]

        return {'exito': True, 'error': None, 'usuario': usuario}