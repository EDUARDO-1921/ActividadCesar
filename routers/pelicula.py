from flask import request, jsonify, render_template
from app import app
from models.pelicula import Pelicula, Genero
from app import login_requerido

#funciones 

#funcion listar
@app.route('/peliculas', methods=['GET'])
def get_peliculas():
    try:
        peliculas = Pelicula.objects()
        return jsonify(peliculas), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 500
    
#funcion agregar 
@app.route('/peliculas/', methods=['POST'])
def agregarPelicula():
    try:
        data = request.get_json(force=True)
        print(data)
        genero = Genero.objects(id=data["genero"]).first()
        print(genero)
        if genero is None:
            return jsonify({"message": "Genero no encontrado"}), 404
        else:
            data["genero"] = genero # Reemplazar el id del genero por el objeto
            pelicula = Pelicula(**data)
            pelicula.save()
            return jsonify(pelicula), 201
    except Exception as e:
        return jsonify({"message": str(e)}), 500
    
#funcion actulizar 
@app.route('/peliculas/<id>', methods=['PUT'])
def actualizarPelicula(id):
    try:
        data = request.get_json(force=True)
        pelicula = Pelicula.objects(id=id).first()
        
        if pelicula is None:
            return jsonify({"message": "Pelicula no encontrada"}), 404
        
        if "genero" in data:
            genero = Genero.objects(id=data["genero"]).first()# obtener el id del genero
            if genero is None:
                return jsonify({"message": "Genero no encontrado"}), 404
            else:
                data["genero"] = genero # reemplazar el id del genero por el objeto
                pelicula.update(**data)
                return jsonify({"message": "Pelicula actualizada"}), 200           
    except Exception as e:
        return jsonify({"message": str(e)}), 500
    
#funcion eliminar 
@app.route('/peliculas/<id>', methods=['DELETE'])
def eliminarPelicula(id):
    try:
        pelicula = Pelicula.objects(id=id).first()
        if pelicula is None:
            return jsonify({"message": "Pelicula no encontrada"}), 404
        else:
            pelicula.delete()
            return jsonify({"message": "Pelicula eliminada"}), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 500
    
#vistas 
#listar pelicula 
@app.route('/listarPeliculas', methods=['GET'])
@login_requerido
def vistaListarPeliculas():
    try:
        peliculas = Pelicula.objects()
        generos = Genero.objects()
        return render_template('listarPelicula.html', peliculas=peliculas, generos=generos), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 500
    
#agregar pelicula 
@app.route('/agregarPelicula/', methods=['GET'])
@login_requerido
def vistaAgregarPelicula():
    try:
        generos = Genero.objects()
        return render_template('agregarPelicula.html', generos=generos), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 500
    
#actulizar pelicula 
@app.route('/addPelicula', methods=['POST'])
def addPelicula():
    try:
        data = request.get_json(force=True)
        genero = Genero.objects(id=data["genero"]).first()
        if genero is None:
            return jsonify({"message": "Genero no encontrado"}), 404
        else:
            data["genero"] = genero
            print(data)
            pelicula = Pelicula(**data) 
            pelicula.save()
            return jsonify({
                "message": "Pelicula guardada",
                "data": pelicula.to_json()  # convierte la película a JSON si es un documento de MongoEngine
            }), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 500 
    
#eliminar pelicula 
@app.route('/eliminarPeliculas/<id>', methods=['GET'])
@login_requerido
def eliminarPeliculas(id):
    try:
        pelicula = Pelicula.objects(id=id).first()
        if pelicula is not  None:
            pelicula.delete()
            return render_template('listarPeliculas.html', peliculas=Pelicula.objects(), generos=Genero.objects()), 200
        else:
            return jsonify({"message": "Pelicula no encontrada"}), 404
    except Exception as e:
        return jsonify({"message": str(e)}), 500
    

@app.route('/editarPeliculas/<id>', methods=['GET'])
@login_requerido
def editarPeliculas(id):  
    try:
        pelicula = Pelicula.objects(id=id).first()
        generos = Genero.objects()
        return render_template('editarPeliculas.html', pelicula=pelicula, generos=generos, genero_seleccionado=pelicula.genero.id), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 500