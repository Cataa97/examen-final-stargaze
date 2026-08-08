from flask import render_template, request, redirect, session, flash
from flask_app import app
from flask_app.models.usuario import Usuario
from flask_app.models.publicacion import Publicacion

@app.route('/dashboard')
def dashboard():
    if 'usuario_id' not in session:
        return redirect('/')

    usuario_actual = Usuario.get_by_id({'id': session['usuario_id']})
    todas_publicaciones = Publicacion.get_all_ordenadas(session['usuario_id'])
    return render_template('dashboard.html', usuario=usuario_actual, publicaciones=todas_publicaciones)

@app.route('/publicaciones/crear', methods=['POST'])
def crear_publicacion():
    if 'usuario_id' not in session:
        return redirect('/')

    if not Publicacion.validar_creacion(request.form):
        return redirect('/dashboard')

    data = {
        'nombre': request.form['nombre'],
        'fecha': request.form['fecha'],
        'lugar': request.form['lugar'],
        'descripcion': request.form['descripcion'],
        'usuario_id': session['usuario_id']
    }
    Publicacion.save(data)
    return redirect('/dashboard')

@app.route('/editar/<int:id>')
def editar_publicacion(id):
    if 'usuario_id' not in session:
        return redirect('/')

    pub = Publicacion.get_by_id({'id': id})
    # bonus1 
    if not pub or pub.usuario_id != session['usuario_id']:
        return redirect('/dashboard')

    return render_template('editar_publicacion.html', pub=pub)

@app.route('/publicaciones/actualizar/<int:id>', methods=['POST'])
def actualizar_publicacion(id):
    if 'usuario_id' not in session:
        return redirect('/')

    pub = Publicacion.get_by_id({'id': id})
    if not pub or pub.usuario_id != session['usuario_id']:
        return redirect('/dashboard')

    if not Publicacion.validar_edicion(request.form, id):
        return redirect(f'/editar/{id}')

    data = {
        'id': id,
        'nombre': request.form['nombre'],
        'fecha': request.form['fecha'],
        'lugar': request.form['lugar'],
        'descripcion': request.form['descripcion'],
        'usuario_id': session['usuario_id']
    }
    Publicacion.update(data)
    return redirect('/dashboard')

@app.route('/publicaciones/borrar/<int:id>')
def borrar_publicacion(id):
    if 'usuario_id' not in session:
        return redirect('/')

    data = {
        'id': id,
        'usuario_id': session['usuario_id']
    }
    Publicacion.delete(data)
    return redirect('/dashboard')

@app.route('/publicaciones/like/<int:id>')
def dar_like(id):
    if 'usuario_id' not in session:
        return redirect('/')

    data = {
        'usuario_id': session['usuario_id'],
        'publicacion_id': id
    }
    Publicacion.add_like(data)
    return redirect('/dashboard')