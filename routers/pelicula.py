from flask import request, render_template, jsonify
from models.pelicula import Pelicula
from models.genero import Genero
from app import app

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/pelicula/", methods=['GET'])
def listPelicula():
    try:
        mensaje = None
        peliculas = Pelicula.objects()
        return render_template('peliculas.html', mensaje=mensaje, peliculas=peliculas)
    except Exception as error:
        mensaje = str(error)
        return render_template('peliculas.html', mensaje=mensaje, peliculas=[])
    
@app.route("/agregarPelicula/", methods=['GET', 'POST'])
def addPelicula():
    try:
        mensaje = None
        estado = False
        generos = Genero.objects()
        
        if request.method == 'POST':
            datos = request.get_json(force=True)
            pelicula = Pelicula(**datos)
            pelicula.save()
            estado = True
            mensaje = "Pelicula agregada correctamente"
            return jsonify({"estado": estado, "mensaje": mensaje})
        
        return render_template('agregarPelicula.html', estado=estado, mensaje=mensaje, generos=generos)
    except Exception as error:
        mensaje = str(error)
        return jsonify({"estado": False, "mensaje": mensaje})

# Nueva ruta para editar película
@app.route("/editarPelicula/<id>", methods=['GET', 'PUT'])
def editarPelicula(id):
    try:
        pelicula = Pelicula.objects(id=id).first()
        generos = Genero.objects()
        
        if request.method == 'PUT':
            datos = request.get_json(force=True)
            pelicula.update(**datos)
            return jsonify({"estado": True, "mensaje": "Película actualizada correctamente"})
        
        return render_template('editarPelicula.html', pelicula=pelicula, generos=generos)
    except Exception as error:
        return jsonify({"estado": False, "mensaje": str(error)})

# Nueva ruta para eliminar película
@app.route("/eliminarPelicula/<id>", methods=['DELETE'])
def eliminarPelicula(id):
    try:
        pelicula = Pelicula.objects(id=id).first()
        pelicula.delete()
        return jsonify({"estado": True, "mensaje": "Película eliminada correctamente"})
    except Exception as error:
        return jsonify({"estado": False, "mensaje": str(error)})