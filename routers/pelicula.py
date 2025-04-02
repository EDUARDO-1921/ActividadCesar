from flask import request,render_template
from models.pelicula import Pelicula
from app import app

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/pelicula/",methods=['GET'])
def listPelicula():
    try:
        mensaje=None
        peliculas=Pelicula.objects()
    except Exception as error:
        mensaje=str(error)
        peliculas=[]
    return render_template('peliculas.html',mensaje=mensaje,peliculas=peliculas)
    
@app.route("/agregarPelicula/",methods=['GET','POST'])
def addPelicula():
    try:
        mensaje=None
        estado=False
        if request.method=='POST':
            datos=request.get_json(force=True)
            pelicula=Pelicula(**datos)
            pelicula.save()
            estado=True
            mensaje="Pelicula Agregado correctamente"
        else:
            mensaje="No permitido"
    except Exception as error:
        mensaje=str(error)
        
    return render_template('agregarPelicula.html',estado=estado,mensaje=mensaje)