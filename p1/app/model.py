from pickleshare import *
from pymongo import MongoClient
from bson.objectid import ObjectId

user_db = PickleShareDB('./usuarios')


class User:
    def __init__(self, usuario, clave):
        self.usuario = usuario
        self.clave = clave

    def crear(self):
        if self.usuario in user_db:
            raise Exception('El usuario ya existe.')
        user_db[self.usuario] = self.clave

    def validar_clave(self):
        valida = user_db[self.usuario] == self.clave
        if not valida:
            raise Exception('Clave incorrecta')


class Pokemon:
    def __init__(self):
        client = MongoClient("mongo", 27017)
        self.db = client.SampleCollections.samples_pokemon

    def get(self, name=None):
        query = {"name": {"$regex": f'{name}', "$options": 'i'}} if name else {}
        pokedex = self.db.find(query)

        pokemon_list = []
        for pokemon in pokedex:
            pokemon_list.append({
                'name': pokemon['name'],
                'img': pokemon['img'],
                'id': str(pokemon['_id'])
            })

        return pokemon_list

    def get_one(self, id):
        pokemon = self.db.find_one({"_id": ObjectId(id)})
        if pokemon is None:
            return None
        return {
            'name': pokemon['name'],
            'img': pokemon['img'],
            'id': str(pokemon['_id'])
        }

    def create(self, data):
        self._validate_pokemon(data)
        self.db.insert(data)

    def _validate_pokemon(self, data):
        if data['name'] is None:
            raise PokemonValidationError('Un pokemon debe tener nombre')
        if data['img'] is None:
            raise PokemonValidationError('Un pokemon debe tener foto')

    def delete(self, id):
        self.db.delete_one({"_id": ObjectId(id)})

    def update(self, id, new_values):
        pokemon = self.get_one(id)
        if pokemon is None:
            return None
        return self.db.update_one({"_id": ObjectId(id)}, {"$set": new_values})


class PokemonValidationError(Exception):
    pass
