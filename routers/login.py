from flask import render_template, request, jsonify, redirect, url_for, session, flash
from werkzeug.security import check_password_hash
from app import app
from models.usuario import Usuario 
import app as dbase

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario_input = request.form['usuario']
        contrasena_input = request.form['clave']

        # Buscar el usuario en la base de datos
        usuario_db = Usuario.objects(usuario=usuario_input).first()

        # Depuración en consola
        print(" Usuario ingresado:", usuario_input)
        print(" Contraseña ingresada:", contrasena_input)

        if usuario_db:
            print(" Usuario encontrado en BD:", usuario_db.usuario)
            print(" Contraseña en BD:", usuario_db.password)

            if usuario_db.password == contrasena_input:
                session['usuario_id'] = str(usuario_db.id)
                session.permanent = True
                flash('Inicio de sesión correcto', 'success')
                print(" SESIÓN GUARDADA:", session)
                return redirect(url_for('listPelicula'))
            else:
                flash('Contraseña incorrecta.', 'error')
                print(" Contraseña incorrecta.")
        else:
            flash('Usuario no encontrado.', 'error')
            print("Usuario no encontrado.")

        return redirect(url_for('login'))

    return render_template('login.html')



#cerrar sesión
@app.route('/logout')
def logout():
    session.pop('usuario_id', None)
    flash('¡Has cerrado sesión!', 'info')
    return redirect(url_for('login'))