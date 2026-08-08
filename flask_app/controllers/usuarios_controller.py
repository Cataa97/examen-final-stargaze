from flask import render_template, request, redirect, session, flash
from flask_app import app, bcrypt
from flask_app.models.usuario import Usuario

@app.route('/')
def index():
    if 'usuario_id' in session:
        return redirect('/dashboard')
    return render_template('index.html')

@app.route('/registro', methods=['POST'])
def registro():
    if not Usuario.validar_registro(request.form):
        return redirect('/')

    password_hash = bcrypt.generate_password_hash(request.form['password']).decode('utf-8')

    data = {
        'nombre': request.form['nombre'],
        'apellido': request.form['apellido'],
        'email': request.form['email'],
        'password': password_hash
    }

    user_id = Usuario.save(data)
    session['usuario_id'] = user_id
    return redirect('/dashboard')

@app.route('/login', methods=['POST'])
def login():
    data = {'email': request.form['email']}
    usuario_db = Usuario.get_by_email(data)

    if not usuario_db:
        flash("Correo o contraseña incorrectos.", "login")
        return redirect('/')

    if not bcrypt.check_password_hash(usuario_db.password, request.form['password']):
        flash("Correo o contraseña incorrectos.", "login")
        return redirect('/')

    session['usuario_id'] = usuario_db.id
    return redirect('/dashboard')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')