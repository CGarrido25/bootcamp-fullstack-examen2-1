from datetime import datetime

from flask import render_template, request ,redirect,session
from flask_app import app,bcrypt  # Importamos la app de la carpeta flask_app

from flask_app.models.usuario import Usuario, crear_usuario,obtener_usuario_por_email, obtener_todos_los_usuarios
from flask_app.models.pelicula import Pelicula, crear_pelicula, obtener_todas_las_peliculas, obtener_pelicula_por_id , editar_pelicula_por_id ,eliminar_pelicula_por_id



@app.route("/nueva", methods=["POST", "GET"])
def nueva_pelicula():
    if "id" not in session:
        return redirect("/inicio")
    if request.method == "GET":   
        return render_template("nueva_pelicula.html",usuario_id=session["id"],tutores=obtener_todos_los_usuarios())
    
    print("**********")
    print(request.form)
    print("**********")
    nombre = request.form['nombre']
    director = request.form['director']
    fecha = request.form['fecha']
    sinopsis = request.form['sinopsis']

    
    pelicula = {
        "nombre": nombre,
        "fecha": fecha,
        "director": director,
        "sinopsis": sinopsis,
        "id_usuario": session["id"],

    }
    
    validaciones =[]
    
    if not nombre:
        validaciones.append("El nombre no puede estar vacío.")
    if not director:
        validaciones.append("El director no puede estar vacío.")
    if not sinopsis:
        validaciones.append("El sinopsis no puede estar vacío.")
    if validaciones:
        return render_template("nueva_pelicula.html",
                                validaciones_registro=validaciones,
                                usuario_id=session["id"],
                                pelicula=pelicula)
    
    id_pelicula_creada = crear_pelicula(pelicula)
    
    if id_pelicula_creada:
        return redirect("/home")
    else:
        return render_template("nueva_pelicula.html",
                               validaciones_registro=["Error al crear la pelicula."])


@app.route("/ver/<int:id>")
def ver_pelicula(id):
    if "id" not in session:
        return redirect("/inicio")
    pelicula = obtener_pelicula_por_id(id)
    
    if pelicula:
        return render_template("ver_pelicula.html", pelicula=pelicula)
    else:
        return redirect("/home")

@app.route("/borrar/<int:id>")
def eliminar_pelicula(id):
    if "id" not in session:
        return redirect("/inicio")
    pelicula = obtener_pelicula_por_id(id)
    if pelicula:
        eliminar_pelicula_por_id(id)
        return redirect("/home")
    else:
        return redirect("/home")
    
@app.route("/editar/<int:id>", methods=["POST", "GET"])
def editar_pelicula(id):
    if "id" not in session:
        return redirect("/inicio")
    if request.method == "GET":
        pelicula = obtener_pelicula_por_id(id)
        if pelicula:
            return render_template("editar_pelicula.html", usuario_id=session["id"], pelicula=pelicula)
        else:
            return redirect("/home")

    # Procesar datos del formulario
    nombre = request.form['nombre']
    director = request.form['director']
    fecha = request.form['fecha']
    sinopsis = request.form['sinopsis']

    pelicula_editar = {
        "id": id,
        "nombre": nombre,
        "director": director,
        "fecha": fecha,
        "sinopsis": sinopsis,
        "id_usuario": session["id"]
    }

    # Validaciones
    validaciones = []
    if not nombre:
        validaciones.append("El nombre no puede estar vacío.")
    if not director:
        validaciones.append("El director no puede estar vacío.")
    if not fecha:
        validaciones.append("La fecha no puede estar vacía.")
    if not sinopsis:
        validaciones.append("La sinopsis no puede estar vacía.")

    if validaciones:
        return render_template("editar_pelicula.html",
                               validaciones_registro=validaciones,
                               usuario_id=session["id"],
                               pelicula=pelicula_editar)

    # Actualizar película en la base de datos
    editar_pelicula_por_id(pelicula_editar)

    return redirect("/home")