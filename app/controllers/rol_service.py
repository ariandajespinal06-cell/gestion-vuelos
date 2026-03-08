from app.models.rol import Rol


REGLAS_ROL = {
    'admin':   'Control total: gestiona usuarios, vuelos y reservas.',
    'agente':  'Gestiona vuelos y reservas; puede consultar usuarios.',
    'cliente': 'Solo puede buscar vuelos, realizar y cancelar sus reservas.',
}


class RolService:
    """Lógica de Negocio para Roles y Permisos del sistema de vuelos"""

    def __init__(self):
        self._rol_repo = Rol()

    def obtener_roles(self):
        return self._rol_repo.obtener_roles()

    def validar_permisos(self, rol_id, permiso_requerido):
        permisos = self._rol_repo.obtener_permisos_de_rol(rol_id)
        return permiso_requerido in [p['nombre'] for p in permisos]

    def descripcion_rol(self, nombre_rol):
        return REGLAS_ROL.get(nombre_rol, 'Rol sin descripción definida.')