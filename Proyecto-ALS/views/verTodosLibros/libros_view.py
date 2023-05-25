import time

import flask
import flask_login
import sirope
from flask import request

from model.messagedto import MessageDto
from model.userdto import Usuario
from model.librodto import libroDto


def get_blprint():
    search = flask.blueprints.Blueprint("verLibros", __name__,
                                        url_prefix="/verLibros",
                                        template_folder="templates",
                                        static_folder="static")
    syrp = sirope.Sirope()

    return search, syrp


verLibros_blprint, srp = get_blprint()


@flask_login.login_required
@verLibros_blprint.route("/")
def search():
    usr = Usuario.current_user()
    libros = list(sirope.Sirope().load_all(libroDto))

    sust = {
        "usr": usr,
        "libros": libros,
    }

    return flask.render_template("verlibros.html", **sust)
@flask_login.login_required
@verLibros_blprint.route("/comentar", methods=["GET"])
def comentar():
    usr = Usuario.current_user()
    titulo_libro = request.args.get("titulo")
    libro  = srp.find_first(libroDto, lambda u: u.titulo == titulo_libro)
    comentarios =[]
    if libro.oids_messages:
        comentarios = list(srp.multi_load(libro.oids_messages))
    time.sleep(1)
    sust = {
        "usr": usr,
        "libro": libro,
        "comentarios": list(comentarios)
    }

    return flask.render_template("comentarLibro.html", **sust)
@flask_login.login_required
@verLibros_blprint.route("/comentar", methods=["POST"])
def publicar():
    usr = Usuario.current_user()
    titulo_libro = request.args.get("titulo")
    libro  = srp.find_first(libroDto, lambda u: u.titulo == titulo_libro)

    if usr:
        autor = usr.email
        comentario = flask.request.form.get("edComentario","")

        if len(comentario.strip()) > 0 :
                comentario = MessageDto(f"{autor}:{comentario}")
                comentario_oid = srp.save(comentario)
                libro.add_message_oid(comentario_oid)
                srp.save(libro)
    comentarios = list(srp.multi_load(libro.oids_messages))
    time.sleep(1)
    sust = {
        "usr": usr,
        "libro": libro,
        "comentarios": comentarios
    }

    return flask.render_template("comentarLibro.html", **sust)
