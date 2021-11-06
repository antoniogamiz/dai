from pickleshare import *

db = PickleShareDB('./basededatos')


class ModeloUsuario:
    @staticmethod
    def crear(usuario, clave):
        if usuario in db:
            raise Exception('El usuario ya existe.')
        db[usuario] = clave

    @staticmethod
    def comprobar_clave(usuario, clave):
        valida = db[usuario] == clave
        if not valida:
            raise Exception('Clave incorrecta')
