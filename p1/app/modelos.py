from pickleshare import *
from pymongo import MongoClient
from bson.objectid import ObjectId

db = PickleShareDB('./basededatos')
client = MongoClient("mongo", 27017)
db_mongo = client.SampleCollections.Sakila_actors


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


class SociosPlantas:

    @staticmethod
    def todos_los_socios(first_name=None):
        # al usar first_name como regex estamos buscando los nombres que
        # contengan lo que pide el usuario
        # usamos $options: i para la busqueda ignore las mayusculas y minusculas
        query = {"FirstName": {"$regex": f'{first_name}', "$options": 'i'}} if first_name else {}
        resultado_db = db_mongo.find(query)

        lista_socios = []
        for socio in resultado_db:
            lista_socios.append({
                'FirstName': socio['FirstName'],
                'LastName': socio['LastName'],
                'phone': socio['phone'],
                'address': socio['address'],
                'id': str(int(socio['_id'])),
            })

        return lista_socios

    @staticmethod
    def buscar_socio_por_id(id):
        socio = db_mongo.find_one({"_id": id})
        socio_no_existe = socio is None
        if socio_no_existe:
            return None
        return {
            'FirstName': socio['FirstName'],
            'LastName': socio['LastName'],
            'phone': socio['phone'],
            'address': socio['address'],
            'id': str(int(socio['_id'])),
        }

    @staticmethod
    def crear_socio(data):
        if data['FirstName'] is None:
            raise Exception('Tienes que incluir un nombre')
        if data['LastName'] is None:
            raise Exception('Tienes que incluir un apellido')
        if data['phone'] is None:
            raise Exception('Tienes que incluir un telefono')
        if data['address'] is None:
            raise Exception('Tienes que incluir una direccion')
        data['_id'] = db_mongo.find().count() + 1
        db_mongo.insert(data)

    @staticmethod
    def borrar_socio(id):
        db_mongo.delete_one({"_id": id})

    @staticmethod
    def actualizar_socio(id, nuevos_datos):
        socio = SociosPlantas.buscar_socio_por_id(id)
        socio_no_existe = socio is None
        if socio_no_existe:
            return None
        return db_mongo.update_one({"_id": id}, {"$set": nuevos_datos})
