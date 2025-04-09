from flask import request, jsonify, render_template, session, flash, redirect
from app import app
from models.usuario import Usuario
import yagmail
import threading
from app import recaptcha
import requests

email = yagmail.SMTP('carlospalechor@gmail.com','yoqdygtmnxvptnjn',encoding='utf-8')
archivo= "files/reporte.pdf"       

@app.route('/usuarios', methods=['GET'])
def get_usuarios():
    try:
        usuarios = Usuario.objects()
        return jsonify(usuarios), 200                                                           
    except Exception as e:
        return jsonify({"message": str(e)}), 500

@app.route('/usuarios', methods=['POST'])
def agregarUsuario():
    try:
        # data = request.get_json(force=True)
        nombre = request.form.get("nombre")
        userId = request.form.get("userId")
        correo = request.form.get("correo")
        password = request.form.get("password")

        # Validaciones básicas opcionales
        if not all([nombre, userId, correo, password]):
            return jsonify({"message": "Faltan datos"}), 400

        # Crear y guardar el usuario en MongoDB
        usuario = Usuario(
            userId=userId,
            nombre=nombre,
            correo=correo,
            password=password
        )
        
        usuario.save()
        flash('Usuario registrado exitosamente.', 'success')
        return render_template('login.html'), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 500

       
def enviarCorreo(destinatario, asunto, mensaje, archivo):
    email.send(to=destinatario, subject=asunto, contents=[mensaje, archivo])

#metodos para inicio de secion y registro de usuario
@app.route('/usuarios/login', methods=['POST'])
def login():
    try:
        data = request.get_json(force=True)

        token = data.get("g-recaptcha-response")
        if not token:
            return jsonify({"message": "Captcha no verificado"}), 400

        # Validar el token con Google
        secret = app.config['GOOGLE_RECAPTCHA_SECRET_KEY']
        payload = {'secret': secret, 'response': token}
        r = requests.post('https://www.google.com/recaptcha/api/siteverify', data=payload)
        result = r.json()

        if not result.get("success"):
            return jsonify({"message": "Captcha no verificado"}), 400

        # Login
        userId = data.get("userId")
        passwordIn = data.get("password")

        if not userId or not passwordIn:
            return jsonify({"message": "Faltan datos"}), 400

        usuario = Usuario.objects(userId=userId).first()
        if usuario is None:
            return jsonify({"message": "Usuario no encontrado"}), 404

        if passwordIn != usuario.password:
            return jsonify({"message": "Contraseña incorrecta"}), 401

        # Sesión y correo
        session["userId"] = usuario.userId
        session["correo"] = usuario.correo
        session["autenticado"] = True
        mensaje = f'Hola, has iniciado sesión en la aplicación. Este es el reporte de tus inicios: {usuario.userId}'
        destinatarios = [usuario.correo, "andresan0328@gmail.com"]
        hilo = threading.Thread(target=enviarCorreo, args=(destinatarios, 'Inicio de sesión', mensaje, archivo))
        hilo.start()
        return jsonify({"message": "Inicio de sesión exitoso"}), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 500


def enviarCorreoRecuperacion(destinatario, asunto, mensaje):
    email.send(to=destinatario, subject=asunto, contents=[mensaje])
  

@app.route('/recuperarPassword', methods=['POST'])  
def recuperar_password():
    try:
        correo = request.form.get('correo')
        usuario = Usuario.objects(correo=correo).first()
        password = request.form.get('password')
        print("Usuario encontrado:", usuario)
        print("contraseña:", password)
        
        if not usuario:
            flash('Correo no registrado.', 'danger')
            return redirect(request.referrer)
        mensaje = f"Hola {usuario.userId},  tu contraseña es: {usuario.password}"
        hilo = threading.Thread(target=enviarCorreoRecuperacion, args=(correo, 'Recuperación de contraseña', mensaje))
        hilo.start()
        flash('Correo enviado con instrucciones para recuperar tu contraseña.', 'success')
        return redirect(request.referrer)
    except Exception as e:
        print("Error:", e)
        flash('Ocurrió un error al enviar el correo.', 'danger')
        return redirect(request.referrer)


@app.route('/usuarios/logout', methods=['POST'])
def logout():
    try:
        session.clear()
        return jsonify({"message": "Sesión cerrada"}), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 500
    

@app.route('/loginVista', methods=['GET'])
def loginVista():
    try:
        return render_template('login.html'), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 500

  
@app.route('/')
def inicio():
    return render_template('login.html')


@app.route('/dash')
def dash():
    return render_template('content.html')