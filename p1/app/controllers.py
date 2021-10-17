from flask import request


def get_user_data_from_request():
    username = request.form.get('username', None)
    if username is None:
        raise Exception('Usuario es obligatorio')

    password = request.form.get('password', None)
    if password is None:
        raise Exception('Clave es obligatoria')

    remember_me = request.form.get('remember_me', False)

    return username, password, remember_me
