import time
import math
import re
from .model import User
from flask import Flask, render_template, request
from .controllers import get_user_data_from_request

app = Flask(__name__)


@app.route('/')
def root():
    return render_template('index.html')


@app.route("/signup", methods=["GET", "POST"])
def show_signup_form():
    if request.method == 'GET':
        return render_template("login.html", action='/signup')

    username, password, remember_me = get_user_data_from_request()

    try:
        user = User(username, password)
        user.crear()
    except Exception as exception:
        return render_template("login.html", action='/signup', error=str(exception))

    return render_template('index.html', title='Registrado!')


@app.route("/login", methods=["GET", "POST"])
def show_login_form():
    if request.method == 'GET':
        return render_template("login.html", action='/login')

    username, password, remember_me = get_user_data_from_request()

    try:
        user = User(username, password)
        user.validar_clave()
    except Exception as exception:
        return render_template("login.html", action='/login', error=str(exception))
    return render_template('index.html', title='Bienvenido!')


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
