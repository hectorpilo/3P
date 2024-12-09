from flask import render_template, request, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from __init__ import app, db
from models import Usuario, Receta, Ingrediente, RecetaIngrediente, FotoReceta

# Configurar Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))

@app.route('/')
def index():
    recetas_recientes = Receta.query.order_by(Receta.created_at.desc()).limit(6).all()
    return render_template('index.html', recetas_recientes=recetas_recientes)

@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if password != confirm_password:
            flash('Las contraseñas no coinciden', 'danger')
            return redirect(url_for('registro'))

        if Usuario.query.filter_by(email=email).first():
            flash('El email ya está registrado', 'danger')
            return redirect(url_for('registro'))

        if Usuario.query.filter_by(username=username).first():
            flash('El nombre de usuario ya está en uso', 'danger')
            return redirect(url_for('registro'))

        hashed_password = generate_password_hash(password)
        nuevo_usuario = Usuario(username=username, email=email, password_hash=hashed_password)
        
        db.session.add(nuevo_usuario)
        db.session.commit()

        flash('Registro exitoso. Por favor inicia sesión', 'success')
        return redirect(url_for('login'))

    return render_template('registro.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        usuario = Usuario.query.filter_by(email=email).first()

        if usuario and check_password_hash(usuario.password_hash, password):
            login_user(usuario)
            flash('Has iniciado sesión correctamente', 'success')
            return redirect(url_for('index'))
        else:
            flash('Email o contraseña incorrectos', 'danger')

    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Has cerrado sesión', 'success')
    return redirect(url_for('index'))

@app.route('/recetas')
def recetas():
    todas_recetas = Receta.query.order_by(Receta.created_at.desc()).all()
    return render_template('recetas.html', recetas=todas_recetas)

@app.route('/receta/<int:receta_id>')
def ver_receta(receta_id):
    receta = Receta.query.get_or_404(receta_id)
    return render_template('ver_receta.html', receta=receta)

@app.route('/nueva-receta', methods=['GET', 'POST'])
@login_required
def nueva_receta():
    if request.method == 'POST':
        titulo = request.form['titulo']
        instrucciones = request.form['instrucciones']
        tiempo_prep = request.form['tiempo_prep']
        porciones = request.form['porciones']

        nueva_receta = Receta(
            titulo=titulo,
            instrucciones=instrucciones,
            tiempo_prep=tiempo_prep,
            porciones=porciones,
            usuario_id=current_user.id
        )

        db.session.add(nueva_receta)
        db.session.commit()

        flash('Receta creada exitosamente', 'success')
        return redirect(url_for('ver_receta', receta_id=nueva_receta.id))

    return render_template('nueva_receta.html') 