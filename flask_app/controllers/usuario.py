from datetime import datetime

from flask import render_template, request ,redirect,session
from flask_app import app,bcrypt  # Importamos la app de la carpeta flask_app

from flask_app.models.usuario import Usuario, crear_usuario,obtener_usuario_por_email, obtener_todos_los_usuarios
from flask_app.models.pelicula import Pelicula, crear_pelicula, obtener_todas_las_peliculas, obtener_pelicula_por_id , editar_pelicula_por_id ,eliminar_pelicula_por_id


import re

@app.route("/inicio")
def registro():
    return render_template("inicio.html")


@app.route("/", methods=["GET",'POST'])
def inicio():
    if "id" in session:
        return redirect("/home")
    if request.method == 'GET':
        return render_template("inicio.html")
    # Obtener los datos del formulario
    nombre = request.form['nombre']
    apellido = request.form['apellido']
    email = request.form['email']
    contrasena1 = request.form["password1"]
    contrasena2 = request.form["password2"]

    # Expresiones regulares para validaciones
    regex_nombre_apellido = r"^[a-zA-Z]{2,}$"  # Solo letras, al menos 2 caracteres
    regex_email = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"  # Formato de correo válido
    regex_contrasena = r"^(?=.*[A-Z])(?=.*\d).+$"  # Al menos una mayúscula y un número

    validaciones =[]
    # Validaciones
    if not re.match(regex_nombre_apellido, nombre):
        validaciones.append("El nombre debe contener solo letras y al menos 2 caracteres.")
        
    if not re.match(regex_nombre_apellido, apellido):
        validaciones.append("El apellido debe contener solo letras y al menos 2 caracteres.")
        
    if not re.match(regex_email, email):
        validaciones.append("El correo electrónico no tiene un formato válido.")
        
    if len(contrasena1) < 8:
        validaciones.append("La contraseña debe tener al menos 8 caracteres.")
    
    if not re.match(regex_contrasena, contrasena1):
        validaciones.append("La contraseña debe incluir al menos una letra mayúscula y un número.")
     
    if contrasena1 != contrasena2:
        validaciones.append("Las contraseñas no coinciden.")
        
    # Si todas las validaciones pasan
    usuario = {
        "nombre": nombre,
        "apellido": apellido,
        "email": email,
        "contrasena": bcrypt.generate_password_hash(contrasena1) 
    }
    
    if not validaciones:
        # Aquí puedes guardar el usuario en la base de datos
        id_usuario_creado=crear_usuario(usuario)
        print("ID del usuario creado:", id_usuario_creado)
        if id_usuario_creado == False:
            return render_template("inicio.html", 
                           validaciones_registro=["El correo electrónico ya está registrado."],
                           usuario=usuario)
        if id_usuario_creado != 0:
            session["id"] = id_usuario_creado
            session["nombre"] = nombre
            session["email"] = email
            return redirect("/home")
        return redirect("/inicio")
    
    
    return render_template("inicio.html", 
                           validaciones_registro=validaciones,
                           usuario=usuario)

@app.route("/home")
def home():
   
    if "id" in session:

        return render_template("home.html", id=session["id"], nombre=session["nombre"], peliculas=obtener_todas_las_peliculas())
    return redirect("/inicio")

@app.route("/cerrar_sesion")
def cerrar_sesion():
    session.clear()
    return redirect("/inicio")


@app.route("/inicio_sesion", methods=["GET", "POST"])
def inicio_sesion():
    
    email = request.form['email']
    contrasena = request.form['contrasena']
    
    usuario = obtener_usuario_por_email(email)
    if usuario == False:
        return render_template("inicio.html", 
                               validaciones_login=["El correo electrónico no está registrado"])
    
    if usuario and bcrypt.check_password_hash(usuario.contrasena, contrasena):
        session["id"] = usuario.id
        session["nombre"] = usuario.nombre
        session["email"] = usuario.email
        return redirect("/home")
    else:
        return render_template("inicio.html", 
                               validaciones_login=["contraseña incorrectos."])


