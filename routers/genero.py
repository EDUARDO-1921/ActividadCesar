from flask import request, jsonify, render_template
from app import app
from models.genero import Genero
from mongoengine import get_connection
from app import login_requerido

#funcion genero
@app.route('/generos', methods=['GET'])
def get_generos():
    try:
        generos = Genero.objects()        
        return jsonify(generos), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 500
    
 #funcion agregar genero    
@app.route('/generos/', methods=['POST'])
def agregarGenero():
    try:
        data = request.get_json(force=True)
        genero = Genero(**data)
        genero.save()
        print(genero)
        return jsonify({"message": "genero guardado"}), 201
    except Exception as e:
        return jsonify({"message": str(e)}), 500
        
#funcion Actulizar genero 
@app.route('/generos/<id>', methods=['PUT'])
def actualizarGenero(id):
    try:
        data = request.get_json(force=True)
        genero = Genero.objects(id=id).first()
        if genero is None:
            return jsonify({"message": "Genero no encontrado"}), 404
        else:
            generoNuevo = genero.update(**data)
            return jsonify({"message": "Genero actualizado"}), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 500
    
# funcion Eliminar genero 
@app.route('/generos/<id>', methods=['DELETE'])
def eliminarGenero(id):
    try:
        genero = Genero.objects(id=id).first()
        if genero is None:
            return jsonify({"message": "Genero no encontrado"}), 404
        else:
            genero.delete()
            return jsonify({"message": "Genero eliminado"}), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 500
    
# vistas 
# listar Generos
@app.route('/generosVista', methods=['GET'])
@login_requerido 
def get_generos_vista():
    try:
        generos = Genero.objects()
        print("genero encontrado" , generos)
        return render_template('listarGenero.html', generos=generos), 200
    except Exception as e:
        return render_template('error.html', error=str(e)), 500
    
#  Agregar Genero 
@app.route('/agregarGeneroVista', methods=['GET'])
@login_requerido
def agregar_genero_vista():
    try:
        return render_template('agregarGenero.html'), 200
    except Exception as e:
        return render_template('error.html', error=str(e)), 500

#actlizar genero
@app.route('/actualizarGeneroVista/<id>', methods=['GET'])
@login_requerido
def actualizar_genero_vista(id):
    try:
        genero = Genero.objects(id=id).first()
        if genero is None:
            return render_template('error.html', error="Genero no encontrado"), 404
        else:
            return render_template('actualizarGenero.html', genero=genero), 200
    except Exception as e:
        return render_template('error.html', error=str(e)), 500

#eliminarGenero
@app.route('/eliminarGenero/<id>', methods=['GET'])
@login_requerido
def eliminar_genero(id):
    try:
        genero = Genero.objects(id=id).first()
        if genero is not  None:
            genero.delete()
            return render_template('listarGenero.html', generos=Genero.objects()), 200
        else:
            genero.delete()
            return jsonify({"message": "genero no encontrado"}), 404
    except Exception as e:
        return render_template('error.html', error=str(e)), 500