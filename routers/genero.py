from flask import request, render_template, jsonify
from models.genero import Genero
from app import app

@app.route("/genero/", methods=['GET'])
def listGenero():
    try:
        mensaje = None
        generos = Genero.objects()
    except Exception as error:
        mensaje = str(error)
        generos = []
    return render_template('listarGenero.html', mensaje=mensaje, generos=generos)
    
@app.route("/agregarGenero/", methods=['GET', 'POST'])
def addGenero():
    try:
        mensaje = None
        estado = False
        if request.method == 'POST':
            datos = request.get_json(force=True)
            genero = Genero(**datos)
            genero.save()
            estado = True
            mensaje = "Genero Agregado correctamente"
        else:
            mensaje = "No permitido"
    except Exception as error:
        mensaje = str(error)
        
    return render_template('agregarGenero.html', estado=estado, mensaje=mensaje)

# Nueva ruta para editar género
@app.route("/editarGenero/<id>", methods=['GET', 'PUT'])
def editarGenero(id):
    try:
        genero = Genero.objects(id=id).first()
        if request.method == 'PUT':
            datos = request.get_json(force=True)
            genero.update(**datos)
            return jsonify({"estado": True, "mensaje": "Género actualizado correctamente"})
        return render_template('editarGenero.html', genero=genero)
    except Exception as error:
        return jsonify({"estado": False, "mensaje": str(error)})

# Nueva ruta para eliminar género
@app.route("/eliminarGenero/<id>", methods=['DELETE'])
def eliminarGenero(id):
    try:
        genero = Genero.objects(id=id).first()
        genero.delete()
        return jsonify({"estado": True, "mensaje": "Género eliminado correctamente"})
    except Exception as error:
        return jsonify({"estado": False, "mensaje": str(error)})
        