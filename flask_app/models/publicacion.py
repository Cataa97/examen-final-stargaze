from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import usuario

class Publicacion:
    def __init__(self, data):
        self.id = data['id']
        self.nombre = data['nombre']
        self.fecha = data['fecha']
        self.lugar = data['lugar']
        self.descripcion = data['descripcion']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.usuario_id = data['usuario_id']
        self.creador = None
        self.num_likes = 0
        self.dio_like = False

    @classmethod
    def save(cls, data):
        query = "INSERT INTO publicaciones (nombre, fecha, lugar, descripcion, usuario_id, created_at, updated_at) VALUES (%(nombre)s, %(fecha)s, %(lugar)s, %(descripcion)s, %(usuario_id)s, NOW(), NOW());"
        return connectToMySQL('esquema_stargaze').query_db(query, data)

    @classmethod
    def get_by_nombre(cls, data):
        query = "SELECT * FROM publicaciones WHERE nombre = %(nombre)s;"
        results = connectToMySQL('esquema_stargaze').query_db(query, data)
        if results:
            return cls(results[0])
        return None

    @classmethod
    def get_all_ordenadas(cls, user_id):
       #bonus por fechas
        query = "SELECT * FROM publicaciones JOIN usuarios ON publicaciones.usuario_id = usuarios.id ORDER BY publicaciones.fecha ASC;"
        results = connectToMySQL('esquema_stargaze').query_db(query)
        publicaciones = []
        if results:
            for fila in results:
                pub_obj = cls(fila)
                data_usuario = {
                    'id': fila['usuarios.id'] if 'usuarios.id' in fila else fila['id'],
                    'nombre': fila['nombre'],
                    'apellido': fila['apellido'],
                    'email': fila['email'],
                    'password': fila['password'],
                    'created_at': fila['usuarios.created_at'] if 'usuarios.created_at' in fila else fila['created_at'],
                    'updated_at': fila['usuarios.updated_at'] if 'usuarios.updated_at' in fila else fila['updated_at']
                }
                pub_obj.creador = usuario.Usuario(data_usuario)

                #bonus likess
                query_likes = "SELECT COUNT(*) as total FROM me_gustas WHERE publicacion_id = %(pub_id)s;"
                res_likes = connectToMySQL('esquema_stargaze').query_db(query_likes, {'pub_id': pub_obj.id})
                if res_likes:
                    pub_obj.num_likes = res_likes[0]['total']
                # bonus si ya le dio mg
                query_user_like = "SELECT * FROM me_gustas WHERE usuario_id = %(user_id)s AND publicacion_id = %(pub_id)s;"
                res_user_like = connectToMySQL('esquema_stargaze').query_db(query_user_like, {'user_id': user_id, 'pub_id': pub_obj.id})
                if res_user_like:
                    pub_obj.dio_like = True
                publicaciones.append(pub_obj)
        return publicaciones

    @classmethod
    def get_by_id(cls, data):
        query = "SELECT * FROM publicaciones WHERE id = %(id)s;"
        results = connectToMySQL('esquema_stargaze').query_db(query, data)
        if results:
            return cls(results[0])
        return None

    @classmethod
    def update(cls, data):
        query = "UPDATE publicaciones SET nombre=%(nombre)s, fecha=%(fecha)s, lugar=%(lugar)s, descripcion=%(descripcion)s, updated_at=NOW() WHERE id = %(id)s AND usuario_id = %(usuario_id)s;"
        return connectToMySQL('esquema_stargaze').query_db(query, data)

    @classmethod
    def delete(cls, data):
        query = "DELETE FROM publicaciones WHERE id = %(id)s AND usuario_id = %(usuario_id)s;"
        return connectToMySQL('esquema_stargaze').query_db(query, data)

    @classmethod
    def add_like(cls, data):
        query = "INSERT INTO me_gustas (usuario_id, publicacion_id) VALUES (%(usuario_id)s, %(publicacion_id)s);"
        return connectToMySQL('esquema_stargaze').query_db(query, data)

    @staticmethod
    def validar_creacion(pub):
        es_valido = True

        if not pub.get('nombre') or len(pub['nombre'].strip()) == 0:
            flash("nombre obligatorio", "publicacion")
            es_valido = False
        else:
           # bonus nombre unico
            existente = Publicacion.get_by_nombre({'nombre': pub['nombre'].strip()})
            if existente:
                flash("este nombre de estrella-constelación ya existe", "publicacion")
                es_valido = False

        if not pub.get('fecha'):
            flash("la fecha es obligatoria", "publicacion")
            es_valido = False

        if not pub.get('lugar') or len(pub['lugar'].strip()) == 0:
            flash("el lugar del encuentro es obligatorio", "publicacion")
            es_valido = False

        if not pub.get('descripcion') or len(pub['descripcion'].strip()) == 0:
            flash("la descripcion del evento es obligatorioa", "publicacion")
            es_valido = False

        return es_valido

    @staticmethod
    def validar_edicion(pub, current_id):
        es_valido = True

        if not pub.get('nombre') or len(pub['nombre'].strip()) == 0:
            flash("El nombre no puede estar vacío", "edicion")
            es_valido = False
        else:
            #bonus nombre puede ser igual al actual pero no a otro
            existente = Publicacion.get_by_nombre({'nombre': pub['nombre'].strip()})
            if existente and str(existente.id) != str(current_id):
                flash("este nombre ya está siendo utilizado por otra publicación", "edicion")
                es_valido = False

        if not pub.get('fecha'):
            flash("la fecha no puede estar vacia", "edicion")
            es_valido = False

        if not pub.get('lugar') or len(pub['lugar'].strip()) == 0:
            flash("el lugar no puede estar vacio", "edicion")
            es_valido = False

        if not pub.get('descripcion') or len(pub['descripcion'].strip()) == 0:
            flash("descripcion obligatoria", "edicion")
            es_valido = False

        return es_valido