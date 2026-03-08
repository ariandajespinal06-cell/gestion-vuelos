import re


class Validaciones:
    """Helper de validaciones para formularios del sistema de vuelos"""

    @staticmethod
    def validar_usuario(datos):
        errores = []

        nombre   = datos.get('nombre', '').strip()
        correo   = datos.get('correo', '').strip()
        password = datos.get('password', '')
        rol_id   = datos.get('rol_id')

        if not nombre:
            errores.append("El nombre es obligatorio.")
        elif len(nombre) < 3:
            errores.append("El nombre debe tener al menos 2 caracteres.")

        if not correo:
            errores.append("El correo electrónico es obligatorio.")
        elif not re.match(r'^[\w\.\+\-]+@[\w\-]+\.[a-z]{2,}$', correo, re.IGNORECASE):
            errores.append("El correo electrónico no tiene un formato válido.")

        if not password:
            errores.append("La contraseña es obligatoria.")
        elif len(password) < 6:
            errores.append("La contraseña debe tener al menos 6 caracteres.")

        if not rol_id:
            errores.append("Favor seleccionar un rol.")
        else:
            try:
                int(rol_id)
            except (ValueError, TypeError):
                errores.append("El rol seleccionado no es válido.")

        return errores

    @staticmethod
    def validar_rol(datos):
        errores = []
        if not datos.get('rol_id'):
            errores.append("El rol es obligatorio.")
        return errores