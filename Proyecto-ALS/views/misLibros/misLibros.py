import time

import flask
import flask_login
import sirope
from flask import request

from model.messagedto import MessageDto
from model.userdto import Usuario
from model.librodto import libroDto


def get_blprint():
    search = flask.blueprints.Blueprint("escribirLibro", __name__,
                                        url_prefix="/misLibros",
                                        template_folder="templates",
                                        static_folder="static")
    syrp = sirope.Sirope()

    return search, syrp


escribirLibro_blprint, srp = get_blprint()


@flask_login.login_required
@escribirLibro_blprint.route("/escribirLibro", methods=["GET"])
def irEscribirLibro():
    usr = Usuario.current_user()

    time.sleep(1)
    sust = {
        "usr": usr,

    }

    return flask.render_template("escribirLibro.html", **sust)
@flask_login.login_required
@escribirLibro_blprint.route("/escribirLibro", methods=["POST"])
def escribirLibro():
    usr = Usuario.current_user()
    if usr:
        autor= usr.email
        titulo = flask.request.form.get("edTituloLibro", "")
        genero = flask.request.form.get("edGeneros")
        sinopsis = flask.request.form.get("edSinopsis", "")
        contenido = flask.request.form.get("edContenido", "")
        libros = srp.filter(libroDto, lambda u: u.titulo == titulo)
        titulo_libros=[]
        for i in libros:
            titulo_libros.append(i.titulo)
        if titulo in titulo_libros:
            flask.flash("ERROR: El titulo del libro ya está cogido!!")
        else:
            if len(titulo.strip()) > 0 and titulo not in titulo_libros and len(genero) > 0 and len(sinopsis.strip()) > 0:
                libro = libroDto( autor,titulo, genero, sinopsis, contenido)
                libro_oid = srp.save(libro)
                usr.add_oid_libro(libro_oid)
                srp.save(usr)
            time.sleep(1)
    return flask.redirect("/misLibros")
@flask_login.login_required
@escribirLibro_blprint.route("/", methods=["GET"])
def verMisLibros():
    usr = Usuario.current_user()
    libros = list(srp.multi_load(usr.get_oids_libros))

    sust = {
        "usr": usr,
        "libros":libros
    }

    return flask.render_template("verMisLibros.html", **sust)

@flask_login.login_required
@escribirLibro_blprint.route("/verLibro", methods=["GET"])
def verLibro():
    usr = Usuario.current_user()
    titulo_libro = request.args.get("titulo")
    libro  = srp.find_first(libroDto, lambda u: u.titulo == titulo_libro)
    sust = {
        "usr": usr,
        "libro": libro
    }

    return flask.render_template("leerLibro.html", **sust)

@flask_login.login_required
@escribirLibro_blprint.route("/eliminar", methods=["POST"])
def eliminar():
    usr = Usuario.current_user()
    titulo_libro = request.args.get("titulo")
    libro  = srp.find_first(libroDto, lambda u: u.titulo == titulo_libro)
    if usr:
        #primero eliminar de la base de datos y de la lista los oids
        for i in libro.oids_messages:
            srp.delete(i)
        libro.borrar_comentarios()
        temp = srp.save(libro)
        for x in usr.get_oids_libros:
            if x == temp:
                srp.delete(temp)
                usr.get_oids_libros.remove(temp)
                srp.save(usr)
    return flask.redirect("/misLibros")
@flask_login.login_required
@escribirLibro_blprint.route("/editarLibro", methods=["GET"])
def editar():
    usr = Usuario.current_user()
    titulo_libro = request.args.get("titulo")
    libro  = srp.find_first(libroDto, lambda u: u.titulo == titulo_libro)
    sust = {
        "usr": usr,
        "libro": libro,
    }

    return flask.render_template("editarLibro.html", **sust)
@flask_login.login_required
@escribirLibro_blprint.route("/editarLibro", methods=["POST"])
def editar2():
    usr = Usuario.current_user()
    if usr:
        titulo = flask.request.form.get("edTituloLibro", "")
        titulo_viejo = request.args.get("titulo")
        libro = srp.find_first(libroDto, lambda u: u.titulo == titulo_viejo)
        genero = flask.request.form.get("edGeneros")
        sinopsis = flask.request.form.get("edSinopsis", "")
        contenido = flask.request.form.get("edContenido", "")
        libros = srp.filter(libroDto, lambda u: u.titulo == titulo)
        titulo_libros = []
        for i in libros:
            titulo_libros.append(i.titulo)
        if titulo in titulo_libros and titulo != titulo_viejo:
            flask.flash("ERROR: El titulo del libro ya está cogido!!")
        else:
            if len(titulo.strip()) > 0  and len(genero) > 0 and len(sinopsis.strip()) > 0:
                libro.set_titulo(titulo)
                libro.set_genero(genero)
                libro.set_sinopsis(sinopsis)
                libro.set_contenido(contenido)
                srp.save(libro)
    return flask.redirect("/misLibros")