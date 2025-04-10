from flask_app.config.my_sql_conection import connectToMySQL

from flask_app.models.usuario import Usuario

class Pelicula:
    def __init__(self, id, nombre,director,fecha, sinopsis ,created_at,updated_at,usuario:Usuario,comentarios=None):
        self.id = id
        self.nombre = nombre
        self.director = director
        self.fecha = fecha
        self.sinopsis = sinopsis
        self.created_at = created_at
        self.updated_at = updated_at
        self.usuario = usuario
        self.comentarios = comentarios if comentarios is not None else []


    def __str__(self):
        return f"Id: {self.id}, Tema: {self.tema}, Fecha: {self.fecha}, Duracion: {self.duracion}, Notas: {self.notas}, Usuario: {self.usuario}, Tutor: {self.tutor}"

class Comentario:
    def __init__(self, id, comentario,fecha, created_at, updated_at):
        self.id = id
        self.comentario = comentario
        self.fecha = fecha
        self.created_at = created_at
        self.updated_at = updated_at


    def __str__(self):
        return f"Id: {self.id}, Contenido: {self.contenido}, Usuario: {self.usuario}"

def crear_pelicula(pelicula):
    query = """INSERT INTO `peliculas`.`peliculas` (`nombre`, `director`, `fecha_estreno`, `sinopsis`, `usuarios_id`) VALUES (%(nombre)s, %(director)s, %(fecha)s, %(sinopsis)s, %(id_usuario)s);"""
    data = {
        "nombre": pelicula['nombre'],
        "director": pelicula['director'],
        "fecha": pelicula['fecha'] if isinstance(pelicula['fecha'], str) else pelicula['fecha'].strftime('%Y-%m-%d'),
        "sinopsis": pelicula['sinopsis'],
        "id_usuario": int(pelicula['id_usuario'])
    }
    print("Query:", query, "Data:", data)  # Imprime la consulta y los datos
    query_result = connectToMySQL("peliculas").query_db(query, data)
    return query_result

def obtener_todas_las_peliculas():
    query = """
    SELECT * FROM peliculas.peliculas AS pelicula
    JOIN usuarios AS usuario ON pelicula.usuarios_id = usuario.id;
    """
    result = connectToMySQL("peliculas").query_db(query)
    peliculas = []
    for row in result:
        usuario = Usuario(
            id=row['usuario.id'],
            nombre=row['usuario.nombre'],
            apellido=row['apellido'],
            email=row['email'],
            contrasena=None,
            created_at=row['usuario.created_at'],
            updated_at=row['usuario.updated_at']
        )

        peliculas.append(Pelicula(
            id=row['id'],
            nombre=row['nombre'],
            director=row['director'],
            fecha=row['fecha_estreno'],
            sinopsis=row['sinopsis'],
            created_at=row['created_at'],
            updated_at=row['updated_at'],
            usuario=usuario
        ))
    return peliculas

def obtener_pelicula_por_id(id):
    query = """
    SELECT * FROM peliculas.peliculas 
    JOIN 
        peliculas.usuarios as usuario ON peliculas.usuarios_id = usuario.id
    WHERE peliculas.id = %(id)s;
    """
    data = {
        "id": id
    }
    result = connectToMySQL("peliculas").query_db(query, data)
    if len(result) == 0:
        return False
    else:
        print(result[0])
        usuario = Usuario(
            id=result[0]['usuario.id'],
            nombre=result[0]['usuario.nombre'],
            apellido=result[0]['apellido'],
            email=result[0]['email'],
            contrasena=None,
            created_at=result[0]['usuario.created_at'],
            updated_at=result[0]['usuario.updated_at']
        )


        pelicula = Pelicula(
            id=result[0]['id'],
            nombre=result[0]['nombre'],
            director=result[0]['director'],
            fecha=result[0]['fecha_estreno'],
            sinopsis=result[0]['sinopsis'],
            created_at=result[0]['created_at'],
            updated_at=result[0]['updated_at'],
            usuario=usuario
        )
        return pelicula

def editar_pelicula_por_id(pelicula):
    query = """
    UPDATE peliculas.peliculas 
    SET nombre = %(nombre)s, director = %(director)s, fecha_estreno = %(fecha)s, sinopsis = %(sinopsis)s, updated_at = NOW() 
    WHERE id = %(id)s;
    """
    data = {
        "nombre": pelicula['nombre'],
        "director": pelicula['director'],
        "fecha": pelicula['fecha'],
        "sinopsis": pelicula['sinopsis'],
        "id": int(pelicula['id'])
    }
    print("Query:", query, "Data:", data)  # Imprime la consulta y los datos
    query_result = connectToMySQL("peliculas").query_db(query, data)
    return query_result

def eliminar_pelicula_por_id(id):
    query = "DELETE FROM peliculas.peliculas WHERE id = %(id)s;"
    data = {"id": id}
    return connectToMySQL("peliculas").query_db(query, data)