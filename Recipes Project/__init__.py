from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config

# Inicializar Flask
app = Flask(__name__)
app.config.from_object(Config)

# Inicializar SQLAlchemy con la app
db = SQLAlchemy(app)

# Importar modelos después de crear db
from models import *