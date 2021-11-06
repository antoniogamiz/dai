from .modelos import ModeloUsuario
import math
import re
from flask import Flask, render_template, request, session, redirect
app = Flask(__name__)
app.secret_key = 'STRING SUPER SECRETO'


TITULO_LOGEADO = 'Bienvenido de nuevo a Planta Elena!'
TITULO_NO_LOGEADO = 'Bienvenido a Planta Elena!'
USUARIO_SE_HA_DESLOGEADO = 'Vuelve pronto!'


def conseguir_usuario():
    return request.form.get('username', None)


def conseguir_contraseña():
    return request.form.get('password', None)


def conseguir_flag_recuerdame():
    return request.form.get('remember_me', False)


@app.route('/')
def hello_plantitas():
    if 'usuario_esta_logeado' in session:
        return render_template('principal.html', titulo=TITULO_LOGEADO, usuario_esta_logeado=True)
    return render_template('principal.html', titulo=TITULO_NO_LOGEADO, usuario_esta_logeado=False)


@app.route("/registrarse", methods=["GET", "POST"])
def mostrar_registrar_usuario():
    if request.method == 'GET':
        return mostrar_pagina_inicio_sesion()

    if request.method == 'POST':
        return registrar_usuario()


def registrar_usuario():
    usuario = conseguir_usuario()
    contraseña = conseguir_contraseña()
    remember_me = conseguir_flag_recuerdame()

    if usuario is None or contraseña is None:
        return render_template("inicio_sesion.html", action='/registrarse', error='Por favor, introduce unos datos válidos.')

    # si el usuario está ya logeado, entonces no debería poder volver a registrarse
    if 'usuario_esta_logeado' in session:
        return redirect("/")

    try:
        ModeloUsuario.crear(usuario, contraseña)
        session['usuario_esta_logeado'] = True
    except Exception as exception:
        return render_template("login.html", action='/registrarse', error=str(exception))

    return render_template('principal.html', titulo='Ya eres miembro de Planta Elena! Hora de comprar :D!')


@app.route("/iniciarsesion", methods=["GET", "POST"])
def show_login_form():
    if request.method == 'GET':
        return mostrar_pagina_inicio_sesion()

    usuario = conseguir_usuario()
    contraseña = conseguir_contraseña()
    remember_me = conseguir_flag_recuerdame()

    # si el usuario esta ya logeado, no puede volver a iniciar sesion
    if 'usuario_esta_logeado' in session:
        return redirect("/")

    try:
        ModeloUsuario.validar_clave(usuario, contraseña)
        session['usuario_esta_logeado'] = True
    except Exception as exception:
        return render_template("iniciosesion.html", action='/iniciarsesion', error=str(exception))

    return render_template('principal.html', title=TITULO_LOGEADO)


def mostrar_pagina_inicio_sesion():
    return render_template("iniciosesion.html", action='/registrarse')


@ app.route('/terminarsesion')
def logout():
    # borramos la clave de la cookie para que la proxima vez que habra la pagina
    # sepamos que el usuario no esta logeado
    session.pop('usuario_esta_logeado', None)
    return render_template('principal.html', titulo=USUARIO_SE_HA_DESLOGEADO, usuario_esta_logeado=False)


# ==============================de la práctica 1 =====================================================

@ app.route('/ordenar/<numeros>')
def ordenar(numeros):
    numeros = numeros.split(",")
    ordenados = sorted(numeros)
    return render_template('ejercicio.html', numero=2, input=numeros, resultado=ordenados)


@ app.route('/primos/<int:n>')
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
    return render_template('ejercicio.html', numero=3, input=n, resultado=resultado)


@ app.route('/secuencia_fibonacci/<int:n>')
def secuencia_fibonacci(n):
    a, b = 1, 1
    if n <= 2:
        return {'n': a}
    for i in range(n-2):
        tmp = a
        a = b
        b = tmp + b
    return render_template('ejercicio.html', numero=4, input=n, resultado=b)


@app.route('/validar_corchetes/<corchetes>')
def corchetes(corchetes):
    contador = 0
    for c in corchetes:
        if c == '[':
            contador += 1
            continue
        contador -= 1

    resultado = 'Inválido' if contador != 0 else 'Válido'
    return render_template('ejercicio.html', numero=5, input=corchetes, resultado=resultado)


@app.route('/identificar/<texto>')
def identificar(texto):
    resultado = ''
    if re.match('[A-Z]\w+ [A-Z]', texto):
        resultado = 'Palabra detectada'
    if re.match("^.+@.+\..+$", texto):
        resultado = 'Correo electronico'
    if re.match("^(\d{4}[- ]?){4}$", texto):
        resultado = 'Tarjeta de credito'
    resultado = 'No se ha encontrado nada'
    return render_template('ejercicio.html', numero=6, input=texto, resultado=resultado)


@app.errorhandler(404)
def own_404_page(error):
    return '404 - Not found'
