from datetime import datetime


class libroDto:
    def __init__(self, autor, titulo, generos, sinopsis, contenido):
        self._autor = autor
        self._titulo = titulo
        self._generos = generos
        self._sinopsis = sinopsis
        self._fecha_creacion = datetime.now()
        self._contenido= contenido
        self._messages_oids = []

    @property
    def autor(self):
        return self._autor

    @property
    def titulo(self):
        return self._titulo

    @property
    def generos(self):
        return self._generos

    @property
    def sinopsis(self):
        return self._sinopsis

    @property
    def fecha_creacion(self):
        return self._fecha_creacion

    @property
    def contenido(self):
        return self._contenido
    @property
    def oids_messages(self):
        if not self.__dict__.get("_messages_oids"):
            self._messages_oids = []
        return self._messages_oids

    def set_titulo(self, valor):
        self._titulo = valor
    def set_genero(self, valor):
        self._generos = valor
    def set_sinopsis(self, valor):
        self._sinopsis = valor
    def set_contenido(self, valor):
        self._contenido = valor
    def borrar_comentarios(self):
        self._messages_oids = []
    def add_message_oid(self, message_oid):
        self.oids_messages.append(message_oid)

    def __str__(self):
        return f"{self.titulo}: \n{self.autor} \n{self.fecha_creacion} \n{self.generos} \n{self.sinopsis}"