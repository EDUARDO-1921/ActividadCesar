from flask import request, render_template, redirect, url_for, session, flash, jsonify
from models.usuario import Usuario
from app import app
import hashlib

# Función para encriptar la contraseña
def encrypt_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Ruta para el login
@app.route("/login/", methods=['GET', 'POST'])
def login():
    mensaje = None
    estado = False
    
    if request.method == 'POST':
        try:
            datos = request.get_json(force=True)
            usuario_input = datos.get('usuario')
            password_input = datos.get('password')
            
            # Buscar el usuario en la base de datos
            usuario = Usuario.objects(usuario=usuario_input).first()
            
            if usuario and usuario.password == password_input:  # En producción deberías usar encriptación
                # Crear sesión
                session['usuario'] = usuario.usuario
                session['nombre'] = usuario.nombre_completo
                estado = True
                mensaje = "Login exitoso"
            else:
                mensaje = "Usuario o contraseña incorrectos"
        except Exception as error:
            mensaje = str(error)
        
        return jsonify({"estado": estado, "mensaje": mensaje})
    
    return render_template('login.html')

# Ruta para cerrar sesión
@app.route("/logout/")
def logout():
    session.clear()
    return redirect(url_for('login'))