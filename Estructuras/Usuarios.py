import webapp2
from google.appengine.ext import ndb
from Recetas import Receta


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

    def add_receta(self, receta):

        m = MiReceta()
        m.id_receta=receta
        m.id_usuario=self.get_id()
        m.put()

    def del_receta(self, receta):
        m = MiReceta.query(MiReceta.id_usuario==self.get_id() and MiReceta.id_receta==receta).fetch()[0]
        m.delete()

    def receta_guardada(self,receta):
        m = MiReceta.query(MiReceta.id_usuario==self.get_id() and MiReceta.id_receta == receta).count()
        print(m)
        if m > 0:
            return True
        else:
            return False

    def get_recetas(self):
        recetas=[]
        mias = MiReceta.query(MiReceta.id_usuario==self.get_id())
        for r in mias:
            recetas.append(Receta.get_by_id(int(r.id_receta)))
        return recetas


class MiReceta(ndb.Model):

    id_receta = ndb.GenericProperty()

    id_usuario = ndb.GenericProperty()

    def delete(self):
        self.key.delete()