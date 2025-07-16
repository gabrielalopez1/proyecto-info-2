from modelo.modelo_datos import ModeloDatos

class Controlador:
    def __init__(self, vista):
        self.vista = vista
        self.modelo = ModeloDatos()

    def verificar_login(self, usuario, clave):
        return self.modelo.validar_usuario(usuario, clave)
