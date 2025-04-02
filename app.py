from flask import Flask
from flask_mongoengine import MongoEngine

app = Flask(__name__)  

app.config["UPLOAD_FOLDER"] = "./static/img"
app.config["MONGODB_SETTINGS"] = [{
    "db": "GestionPeliculas",
    "host": "localhost",
    "port": 27017
}]

db = MongoEngine(app)

if __name__ == "__main__":
    from routers.genero import *
    from routers.pelicula import * 
    app.run(port=6510, host="0.0.0.0", debug=True)
