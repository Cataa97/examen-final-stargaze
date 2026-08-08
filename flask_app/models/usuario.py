from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
NOMBRE_REGEX = re.compile(r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$')

class Usuario:
    def __init__(self, data):
        self.id = data['id']
        self.nombre = data['nombre']
        self.apellido = data['apellido']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def save(cls, data):
        query = "INSERT INTO usuarios (nombre, apellido, email, password, created_at, updated_at) VALUES (%(nombre)s, %(apellido)s, %(email)s, %(password)s, NOW(), NOW());"
        return connectToMySQL('esquema_stargaze').query_db(query, data)

    @classmethod
    def get_by_email(cls, data):
        query = "SELECT * FROM usuarios WHERE email = %(email)s;"
        results = connectToMySQL('esquema_stargaze').query_db(query, data)
        if results:
            return cls(results[0])
        return None

    @classmethod
    def get_by_id(cls, data):
        query = "SELECT * FROM usuarios WHERE id = %(id)s;"
        results = connectToMySQL('esquema_stargaze').query_db(query, data)
        if results:
            return cls(results[0])
        return None

    @staticmethod
    def validar_registro(usuario):
        es_valido = True

        if len(usuario['nombre']) < 2:
            flash("el nombre debe tener al menos 2 caracteres cmo minimo", "registro")
            es_valido = False
        elif not NOMBRE_REGEX.match(usuario['nombre']):
            flash("el nombre solo debe contener letras.", "registro")
            es_valido = False

        if len(usuario['apellido']) < 2:
            flash("el apellido debe tener al menos 2 caracteres como minimo", "registro")
            es_valido = False
        elif not NOMBRE_REGEX.match(usuario['apellido']):
            flash("el apellido solo debe contener letras.", "registro")
            es_valido = False

        if not EMAIL_REGEX.match(usuario['email']):
            flash("formato de correo invalido", "registro")
            es_valido = False
        else:
            usuario_existente = Usuario.get_by_email({'email': usuario['email']})
            if usuario_existente:
                flash("este correo ya está registrado", "registro")
                es_valido = False

        if len(usuario['password']) < 8:
            flash("la contraseña debe tener al menos 8 caracteres", "registro")
            es_valido = False

        if usuario['password'] != usuario['confirm_password']:
            flash("la contraseñas no coinciden, vuelva a ingresarlas", "registro")
            es_valido = False

        return es_valido