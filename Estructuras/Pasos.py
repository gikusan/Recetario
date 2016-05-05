import webapp2
from google.appengine.ext import ndb

# Clase para los pasos
class Paso(ndb.Model):

    # Descripcion del paso
    descripcion = ndb.StringProperty()

    # Tiempo en segundos
    tiempo = ndb.IntegerProperty()

    # Orden en la receta
    orden = ndb.IntegerProperty()

    # Id de la receta a la que pertenece
    id_receta = ndb.GenericProperty()

    def get_id(self):
        return self.key.id()

    def get_id_as_str(self):

        return self.key.id().__str__