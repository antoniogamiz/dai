import time
import math
import re
from flask import Flask
app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'P1 - Antonio Gamiz Delgado'


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
                app.logger.info(f'{i}-{j}')
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
