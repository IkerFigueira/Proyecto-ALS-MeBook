import json

import flask
import flask_login
import sirope
from flask_login import login_manager

from src.model.messagedto import MessageDto
from src.model.userdto import Usuario
import src.views.verTodosLibros.libros_view as libros_view
import src.views.misLibros.misLibros as misLibros
def create_app():
    lmanager = login_manager.LoginManager()
    fapp = flask.Flask(__name__, instance_relative_config=True)
    syrp = sirope.Sirope()

    fapp.config.from_file("config.json",load=json.load)
    lmanager.init_app(fapp)
    fapp.register_blueprint(libros_view.verLibros_blprint)
    fapp.register_blueprint(misLibros.escribirLibro_blprint)
    return fapp, lmanager, syrp


app, lm, srp = create_app()


@lm.user_loader
def user_loader(email):
    return Usuario.find(srp, email)


@app.route('/')
def get_index():
    usr = Usuario.current_user()

    sust = {
        "usr": usr,
    }

    return flask.render_template("index.html", **sust)
@app.route('/registrarse')
def registrarse():
    usr = Usuario.current_user()
    sust = {
        "usr": usr,
    }
    return flask.render_template("registrarse.html", **sust)
@app.route('/registrarse', methods=["POST"])
def registrarse2():
    email_txt = flask.request.form.get("edEmail")
    password_txt = flask.request.form.get("edPassword")
    conf_pass = flask.request.form.get("edPassword2")
    if not email_txt:
        flask.flash("Error: introduce un usuario")
        return flask.redirect("/registrarse")
    else:
        usr = Usuario.find(srp, email_txt)
        if usr:
            flask.flash("Error: el usuario ya existe")
            return flask.redirect("/registrarse")
        if not password_txt:
            flask.flash("Error: No has introducido una contraseña")
            return flask.redirect("/registrarse")
        if not conf_pass:
            flask.flash("Error: No has confirmado la contraseña")
            return flask.redirect("/registrarse")
        if conf_pass != password_txt:
            flask.flash("Error: Las contraseñas no coinciden")
            return flask.redirect("/registrarse")
        if not usr:
            usr = Usuario(email_txt, password_txt)
            srp.save(usr)
        flask_login.login_user(usr)
    srp.save(usr)
    return flask.redirect("/verLibros")

@app.route("/login", methods=["POST"])
def login():
    email_txt = flask.request.form.get("edEmail")
    password_txt = flask.request.form.get("edPassword")

    if not email_txt:
        usr = Usuario.current_user()

        if not usr:
            flask.flash("Error: Tienes que logearte primero")
            return flask.redirect("/")
    else:
        usr = Usuario.find(srp, email_txt)
        if not password_txt:
            flask.flash("Error: No has introducido una contraseña")
            return flask.redirect("/")
        elif not usr:
            flask.flash("Error: El usuario no existe, registrate primero")
            return flask.redirect("/")
        elif not usr.chk_password(password_txt):
            flask.flash("Error: La contraseña es incorrecta")
            return flask.redirect("/")

        flask_login.login_user(usr)
    srp.save(usr)
    return flask.redirect("/verLibros")

@app.route('/logout')
def logout():
    flask_login.logout_user()
    flask.flash("User logged out")
    return flask.redirect("/")


@lm.unauthorized_handler
def unauthorized_handler():
    flask.flash("Unauthorized")
    return flask.redirect("/")


if __name__ == '__main__':
    app.run()
