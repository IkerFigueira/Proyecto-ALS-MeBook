
import sirope
import flask_login
import werkzeug.security as safe


class Usuario(flask_login.UserMixin):
    def __init__(self, email, password):
        self._email = email
        self._password = safe.generate_password_hash(password)
        self._oids_libros = []

    @property
    def email(self):
        return self._email

    @property
    def get_oids_libros(self):
        return self._oids_libros

    def get_id(self):
        return self.email

    def chk_password(self, pswd):
        return safe.check_password_hash(self._password, pswd)

    def add_oid_libro(self, oid_libro):
        self._oids_libros.append(oid_libro)
    @staticmethod
    def current_user():
        usr = flask_login.current_user

        if usr.is_anonymous:
            flask_login.logout_user()
            usr = None

        return usr

    @staticmethod
    def find(s: sirope.Sirope, email: str) -> "Usuario":
        return s.find_first(Usuario, lambda u: u.email == email)
