from datetime import datetime
from flask_login import UserMixin
from __init__ import db

class Usuario(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.Text(length=4294967295), nullable=False)
    created_at = db.Column(db.TIMESTAMP, default=datetime.utcnow)
    recetas = db.relationship('Receta', backref='usuario', lazy=True)

class Receta(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100), nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    instrucciones = db.Column(db.Text, nullable=False)
    tiempo_prep = db.Column(db.Integer)  # en minutos
    porciones = db.Column(db.Integer)
    created_at = db.Column(db.TIMESTAMP, default=datetime.utcnow)
    fotos = db.relationship('FotoReceta', backref='receta', lazy=True)
    ingredientes = db.relationship('RecetaIngrediente', backref='receta', lazy=True)

class Ingrediente(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False, unique=True)
    unidad_medida = db.Column(db.String(20))
    calorias = db.Column(db.Float)

class RecetaIngrediente(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    receta_id = db.Column(db.Integer, db.ForeignKey('receta.id'), nullable=False)
    ingrediente_id = db.Column(db.Integer, db.ForeignKey('ingrediente.id'), nullable=False)
    cantidad = db.Column(db.Float, nullable=False)
    ingrediente = db.relationship('Ingrediente', backref='recetas_link')

class FotoReceta(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    receta_id = db.Column(db.Integer, db.ForeignKey('receta.id'), nullable=False)
    url_imagen = db.Column(db.String(255), nullable=False)
    descripcion = db.Column(db.Text)
    created_at = db.Column(db.TIMESTAMP, default=datetime.utcnow) 