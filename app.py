from flask import Flask, session, request, redirect
from flask_mongoengine import MongoEngine
import os

app = Flask(__name__)  
app.config["UPLOAD_FOLDER"] = "./static/img"
app.config["MONGODB_SETTINGS"] = [{
    "db": "GestionPeliculas",
    "host": "localhost",
    "port": 27017
}]
app.secret_key = "clave_secreta_para_sesiones"  # Clave para sesiones

db = MongoEngine(app)

# Middleware para verificar sesión en todas las rutas
@app.before_request
def check_session():
    # Rutas exentas de verificación de sesión
    exempt_routes = ['login', 'static']
    
    if request.endpoint not in exempt_routes and 'usuario' not in session:
        if request.path != '/login/':
            return redirect('/login/')

if __name__ == "__main__":
    from routers.genero import * 
    from routers.pelicula import *
    from routers.usuario import * # Importar las rutas de usuario
    app.run(port=6510, host="0.0.0.0", debug=True)