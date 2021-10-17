from pickleshare import *

db = PickleShareDB('./usuarios')


class User:
    def __init__(self, usuario, clave):
        self.usuario = usuario
        self.clave = clave

    def crear(self):
        if self.usuario in db:
            raise Exception('El usuario ya existe.')
        db[self.usuario] = self.clave

    def validar_clave(self):
        valida = db[self.usuario] == self.clave
        if not valida:
            raise Exception('Clave incorrecta')
