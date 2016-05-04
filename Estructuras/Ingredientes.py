import webapp2
from google.appengine.ext import ndb
from Estructuras.Pasos import Paso


class Ingrediente(ndb.Model):

    # Id de la receta a la que pertenece el ingrediente
    id_receta = ndb.GenericProperty()

    # Nombre de la receta
    nombre = ndb.StringProperty()

    # Descripcion del ingrediente (opcional)
    descripcion = ndb.StringProperty()

    # Etiquetas de la receta
    cantidad = ndb.StringProperty()

    """
        Funcion para obtener directamente el id del objeto
    """
    def get_id(self):

        return self.key.id()
