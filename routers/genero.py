from flask import request,render_template
from models.genero import Genero
from app import app

@app.route("/genero/",methods=['GET'])
def listGenero():
    try:
        mensaje=None
        generos=Genero.objects()
    except Exception as error:
        mensaje=str(error)
    return render_template('listarGenero.html',mensaje=mensaje,generos=generos)
    
@app.route("/Agregarloro/",methods=['GET'])
def addGenero():
    try:
        mensaje=None
        estado=False
        if request.method=='POST':
            datos=request.get_json(force=True)
            genero=Genero(**datos)
            genero.save()
            estado=True
            mensaje="Genero Agregado correctamente"
        else:
            mensaje="No permitido"
    except Exception as error:
        mensaje=str(error)
        
    return render_template ('agregarGenero.html',estado=estado,mensaje=mensaje)
        