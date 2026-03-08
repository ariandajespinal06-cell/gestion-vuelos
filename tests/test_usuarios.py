import sys
import os
import unittest
from unittest.mock import MagicMock

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.helpers.validaciones import Validaciones
from app.controllers.usuario_facade import UsuarioFacade
from app.controllers.rol_service import RolService


class TestValidaciones(unittest.TestCase):

    def test_datos_validos(self):
        datos = {'nombre': 'Ana Díaz', 'correo': 'ana@vuelos.com',
                 'password': 'pass123', 'rol_id': '2'}
        self.assertEqual(Validaciones.validar_usuario(datos), [])

    def test_nombre_vacio(self):
        datos = {'nombre': '', 'correo': 'x@x.com', 'password': '123456', 'rol_id': '1'}
        errores = Validaciones.validar_usuario(datos)
        self.assertTrue(any('nombre' in e.lower() for e in errores))

    def test_correo_invalido(self):
        datos = {'nombre': 'Juan', 'correo': 'no-es-correo', 'password': '123456', 'rol_id': '1'}
        errores = Validaciones.validar_usuario(datos)
        self.assertTrue(any('correo' in e.lower() for e in errores))

    def test_password_corta(self):
        datos = {'nombre': 'Juan', 'correo': 'x@x.com', 'password': '123', 'rol_id': '1'}
        errores = Validaciones.validar_usuario(datos)
        self.assertTrue(any('contraseña' in e.lower() for e in errores))


class TestUsuarioFacade(unittest.TestCase):

    def _facade_con_mocks(self):
        facade = UsuarioFacade.__new__(UsuarioFacade)
        facade._usuario_service = MagicMock()
        facade._rol_service     = MagicMock()
        return facade

    def test_crear_usuario_exitoso(self):
        facade = self._facade_con_mocks()
        facade._usuario_service.crear_usuario.return_value = {
            'exito': True, 'id': 7, 'error': None
        }
        facade._usuario_service.asignar_permisos.return_value = [
            {'nombre': 'realizar_reserva'}, {'nombre': 'ver_vuelos'}
        ]
        datos = {'nombre': 'Laura Torres', 'correo': 'laura@vuelos.com',
                 'password': 'vuelos99', 'rol_id': '3'}
        resultado = facade.crear_usuario(datos)
        self.assertTrue(resultado['exito'])
        self.assertEqual(resultado['id'], 7)

    def test_validacion_falla_no_llama_servicio(self):
        facade = self._facade_con_mocks()
        datos = {'nombre': '', 'correo': '', 'password': '', 'rol_id': ''}
        resultado = facade.crear_usuario(datos)
        self.assertFalse(resultado['exito'])
        facade._usuario_service.crear_usuario.assert_not_called()


class TestRolService(unittest.TestCase):

    def _service_con_mock(self):
        svc = RolService.__new__(RolService)
        svc._rol_repo = MagicMock()
        return svc

    def test_descripcion_admin(self):
        svc = self._service_con_mock()
        desc = svc.descripcion_rol('admin')
        self.assertIn('total', desc.lower())

    def test_descripcion_cliente(self):
        svc = self._service_con_mock()
        desc = svc.descripcion_rol('cliente')
        self.assertIn('reserva', desc.lower())


if __name__ == '__main__':
    unittest.main(verbosity=2)