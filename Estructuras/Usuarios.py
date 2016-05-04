import webapp2
from google.appengine.ext import ndb


class Usuario(ndb.Model):

    nick = ndb.StringProperty()
    password = ndb.StringProperty()
    email = ndb.StringProperty()
    question = ndb.IntegerProperty()
    respuesta= ndb.StringProperty()
    activado = ndb.StringProperty()
    date = ndb.DateTimeProperty(auto_now_add=True)

    def get_id_as_str(self):

        return self.key.id().__str__()


