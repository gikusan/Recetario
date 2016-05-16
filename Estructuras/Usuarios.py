import webapp2
from google.appengine.ext import ndb


class Usuario(ndb.Model):

    # Nick del usuario
    nick = ndb.StringProperty()

    # Nombre del usuario
    name = ndb.StringProperty()

    # Apellido del usuario
    surname = ndb.StringProperty()

    # Password del usuario
    password = ndb.StringProperty()

    # Email del usuario
    email = ndb.StringProperty()

    # Id de la pregunta del usuario
    question = ndb.GenericProperty()

    # Respuesta a la pregunta secreta
    respuesta= ndb.StringProperty()

    # Usuario activado o no
    activado = ndb.BooleanProperty()

    # rol
    rol = ndb.StringProperty()

    # Fecha de registro del usuario
    date = ndb.DateTimeProperty(auto_now_add=True)

    """
        Funcion que devuelve el id del usuario, tipo Long
    """
    def get_id(self):
        return self.key.id()

    """
        Funcion que devuelve el id como string
    """
    def get_id_as_str(self):

        return self.key.id().__str__

    """
        Funcion que devuelve activado
    """
    def get_activado(self):

        return self.activado.id()
