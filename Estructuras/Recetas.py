import webapp2
from google.appengine.ext import ndb


class Receta(ndb.Model):

    id_usuario = ndb.GenericProperty()
    id_categoria = ndb.StringProperty()
    nombre = ndb.StringProperty()
    etiquetas = ndb.StringProperty()

    def getid(self):

        return self.key.id()
