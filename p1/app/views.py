from flask_restful import Resource, reqparse
from .model import Pokemon


class PokemonView(Resource):
    def get(self, id=None):
        pokemon_model = Pokemon()
        if id is not None:
            pokemon = pokemon_model.get_one(id)
            if pokemon is None:
                return {'message': 'Not found'}, 404
            return pokemon
        return pokemon_model.get()

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, help='Name of the pokemon')
        parser.add_argument('img', type=str, help='URL of the pokemon photo')
        args = parser.parse_args()

        try:
            pokemon_model = Pokemon()
            new_pokemon = {
                'name': args['name'],
                'img': args['img']
            }
            pokemon_model.create(new_pokemon)
            return {"message": "Success!"}, 200
        except Exception as exception:
            return {"message": str(exception)}, 500

    def delete(self, id=None):
        if id is None:
            return {'message': 'You need to provide an id'}, 400
        pokemon_model = Pokemon()
        pokemon_model.delete(id)

    def patch(self, id=None):
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, help='Name of the pokemon')
        parser.add_argument('img', type=str, help='URL of the pokemon photo')
        args = parser.parse_args()

        if id is None:
            return {'message': 'You need to provide an id'}, 400
        pokemon_model = Pokemon()
        new_values = {}
        if args['name']:
            new_values['name'] = args['name']
        if args['img']:
            new_values['img'] = args['img']
        success = pokemon_model.update(id, new_values)
        if success is None:
            return {'message': 'Not found'}, 404

        return {"message": "Success!"}, 200
