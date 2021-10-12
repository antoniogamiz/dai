import math
import re
from flask import Flask
app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Elena Merelo Moline - Práctica 1'


@app.route('/ordenar/<numeros>')
def ordenar(numeros):
    numeros = numeros.split(",")
    ordenados = sorted(numeros)
    return {'resultado': ordenados}


@app.route('/primos/<int:n>')
def primos(n):
    primos = [True for i in range(n + 1)]
    p = 2
    while (p * p <= n):
        if (primos[p] == True):
            for i in range(p ** 2, n + 1, p):
                primos[i] = False
        p += 1
    primos[0] = False
    primos[1] = False
    resultado = [p for p in range(n+1) if primos[p]]
    return {'primos': resultado}


@app.route('/secuencia_fibonacci/<int:n>')
def secuencia_fibonacci(n):
    a, b = 1, 1
    if n <= 2:
        return {'n': a}
    for i in range(n-2):
        tmp = a
        a = b
        b = tmp + b
    return {
        'n': b
    }


@app.route('/validar_corchetes/<corchetes>')
def corchetes(corchetes):
    contador = 0
    for c in corchetes:
        if c == '[':
            contador += 1
            continue
        contador -= 1

    if contador != 0:
        return {'resultado': 'Invalido'}
    return {'resultado': 'Valido'}


@app.route('/identificar/<texto>')
def identificar(texto):
    if re.match('[A-Z]\w+ [A-Z]', texto):
        return 'Palabra detectada'
    if re.match("^.+@.+\..+$", texto):
        return 'Correo electronico'
    if re.match("^(\d{4}[- ]?){4}$", texto):
        return 'Tarjeta de credito'
    return 'No se ha encontrado nada'


@app.errorhandler(404)
def own_404_page(error):
    return '404 - Not found'
