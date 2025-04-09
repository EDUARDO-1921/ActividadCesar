from flask import Flask, render_template, session, jsonify, flash
from flask_mongoengine import MongoEngine
from functools import wraps
from dotenv import load_dotenv
from google_recaptcha_flask import ReCaptcha
from flask_cors import CORS
from mongoengine.connection import get_db
import os

load_dotenv()

app = Flask(__name__) 
CORS(app, resources={r"/*": {"origins": "*"}})  # Permitir cualquier ruta

# Variables de entorno
key = os.environ.get("SECRET_KEY")
user = os.environ.get("USER_BD")
uri = ""  

# Configuración base
app.secret_key = key  
app.config['SESSION_TYPE'] = 'filesystem' 
app.config["UPLOAD_FOLDER"] = "./static/images"

app.config['MONGODB_SETTINGS'] = [{
    "db": "GestionPeliculas",
    "host": uri,

}]

app.config['CORS_HEADERS'] = 'Content-Type'

#Configurar reCAPTCHA desde variables .env
app.config['GOOGLE_RECAPTCHA_ENABLED'] = True
app.config['GOOGLE_RECAPTCHA_SITE_KEY'] = os.environ.get("RECAPTCHA_SITE_KEY")
app.config['GOOGLE_RECAPTCHA_SECRET_KEY'] = os.environ.get("RECAPTCHA_SECRET_KEY")

# Inicializacion extensiones
recaptcha = ReCaptcha(app=app)
db = MongoEngine(app)
db_actual = get_db()

print("Coneccion exitosa a la base datos:", db_actual.name)

# Decorador para rutas protegidas
def login_requerido(f):
    @wraps(f)
    def decorador(*args, **kwargs):
        if "autenticado" not in session or not session["autenticado"]:
            flash("Debes iniciar sesión para acceder a esta página.", "danger")
            return render_template('login.html'), 401
        return f(*args, **kwargs)
    return decorador

from routers.pelicula import *
from routers.genero import *
from routers.usuario import *

if __name__ == '__main__':
    app.run(port=5000, host='0.0.0.0', debug=True)
