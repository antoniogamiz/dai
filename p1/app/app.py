import time
import math
import re
from .model import User, Pokemon
from flask import Flask, render_template, request, session, redirect
from flask_restful import Resource, Api
from .controllers import get_user_data_from_request
from .views import PokemonView

app = Flask(__name__)
api = Api(app)
app.secret_key = 'esto-es-una-clave-muy-secreta'
api.add_resource(PokemonView, '/pokemon', '/pokemon/<id>')


@app.route('/')
def root():
    return render_home_page()


@app.route('/pokemon_catalog', methods=["GET", "POST"])
def pokemon():
    pokemon_model = Pokemon()
    name = request.form.get('pokemon_name', None)
    pokemons = pokemon_model.get(name)
    return render_template('pokemon.html', name=name or '', pokemons=pokemons, title='Pokemon', logeado='logeado' in session)


@app.route("/signup", methods=["GET", "POST"])
def show_signup_form():
    if request.method == 'GET':
        return render_template("login.html", action='/signup')

    username, password, remember_me = get_user_data_from_request()

    if 'logeado' in session:
        return redirect("/")

    try:
        user = User(username, password)
        user.crear()
        session['logeado'] = True

    except Exception as exception:
        return render_template("login.html", action='/signup', error=str(exception))

    return render_template('index.html', title='Registrado!')


@app.route("/login", methods=["GET", "POST"])
def show_login_form():
    if request.method == 'GET':
        return render_template("login.html", action='/login')

    username, password, remember_me = get_user_data_from_request()

    if 'logeado' in session:
        return redirect("/")

    try:
        user = User(username, password)
        user.validar_clave()
        session['logeado'] = True
    except Exception as exception:
        return render_template("login.html", action='/login', error=str(exception))
    return render_template('index.html', title='Bienvenido!')


@app.route('/logout')
def logout():
    session.pop('logeado', None)
    return redirect("/")


# ejercicio 2
@app.route('/ordenar/<numeros>')
def ordenar(numeros):
    numeros = numeros.split(",")

    start_time = time.perf_counter()
    numeros.sort()
    end_time = time.perf_counter()

    return {
        'sorted': numeros,
        'time': end_time-start_time
    }


# ejercicio 3
@app.route('/erastotenes/<int:n>')
def erastotenes(n):
    marcas = [0] * n
    for i in range(2, math.floor(math.sqrt(n))+1):
        if not marcas[i-1]:
            for j in range(i, n // i + 1):
                marcas[i*j - 1] = 1
    resultado = [i+1 for i, x in enumerate(marcas) if x == 0 and i != 0]
    return {'resultado': resultado}


# ejercicio 4
@app.route('/fibonacci/<int:n>')
def fibonacci(n):
    phi = (1+math.sqrt(5))/2
    n_plus_1 = (pow(phi, n) - pow(1-phi, n)) / math.sqrt(5)
    return {
        'resultado': int(n_plus_1)
    }


# ejercicio 5
@app.route('/corchetes/<corchetes>')
def corchetes(corchetes):
    contador = 0
    for c in corchetes:
        if c == '[':
            contador += 1
        else:
            contador -= 1

        if contador < 0:
            return {'resultado': 'Invalido'}

    if contador != 0:
        return {'resultado': 'Invalido'}
    return {'resultado': 'Valido'}


# ejercicio 6
@app.route('/regulares/<texto>')
def regulares(texto):
    if re.match('[A-Z]\w+ [A-Z]', texto):
        return {'resultado': 'Palabra detectada'}
    if re.match("^.+@.+\..+$", texto):
        return {'resultado': 'Es un correo electronico'}
    if re.match("^(\d{4}[- ]?){4}$", texto):
        return {'resultado': 'Es una tarjeta de credito'}
    return {'resultado': 'El texto introducido no es ni una palabra en mayuscula seguida de mayuscula, ni un email ni una tarjeta de credito.'}


@app.errorhandler(404)
def own_404_page(error):
    return 'KERNEL PANIC - PAGINA NO ENCONTRADA!!!'


def render_home_page(title='Lore ipsum'):
    if 'logeado' in session:
        return render_template('index.html', title=title, logeado=True)
    return render_template('index.html', title='Lore ipsum', logeado=False)
