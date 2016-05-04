import webapp2
from google.appengine.ext import ndb


class Usuario(ndb.Model):

    # Nick del usuario
    nick = ndb.StringProperty()

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


