import webapp2
from google.appengine.ext import ndb
from Estructuras.Pasos import Paso
from Estructuras.Ingredientes import Ingrediente


class Receta(ndb.Model):

    # Id del usuario propietario de la receta
    id_usuario = ndb.GenericProperty()

    # Id de la categoria a la que pertenece la receta
    id_categoria = ndb.StringProperty()

    # Nombre de la receta
    nombre = ndb.StringProperty()

    # Nombre de la receta
    descripcion = ndb.StringProperty()

    # Etiquetas de la receta
    etiquetas = ndb.StringProperty()

    # Clave para buscar la foto
    blob_key = ndb.BlobKeyProperty()

    # Para controlar el numero de pasos
    num_pasos = ndb.IntegerProperty()

    # Para controlar el numero de votos
    num_votos = ndb.IntegerProperty()

    def delete(self):
        return self.key.delete()

    """
        Funcion para obtener directamente el id del objeto
    """
    def get_id(self):

        return self.key.id()

    """
        Funcion para insertar un paso a partir de una receta
    """
    def insertar_paso(self,desc,temp):

        p = Paso(descripcion=desc,tiempo=temp,orden=self.num_pasos,id_receta=self.get_id())
        self.num_pasos += 1
        p.put()
        self.put()


    """
        Funcion para insertar un paso a partir de una receta
    """

    def insertar_ingrediente(self, nombre, cantidad, descripcion):
        i = Ingrediente(nombre=nombre, cantidad=cantidad, descripcion=descripcion, id_receta=self.get_id())
        i.put()

    """
        Funcion para obtener los pasos de la receta en orden
    """
    def obtener_pasos(self):

        return Paso.query(Paso.id_receta==self.get_id()).order(Paso.orden)

    """
        Funcion para obtener los ingredientes de la receta
    """

    def obtener_ingredientes(self):
        return Ingrediente.query(Ingrediente.id_receta == self.get_id())

    """
        Funcion para votar
    """
    def add_voto(self):
        self.num_votos += 1
        self.put()

    """
        Funcion para anadir comentarios
    """
    def add_comentario(self,texto,usuario):
        i = Comentario()
        i.id_receta = self.get_id()
        i.nick = usuario
        i.texto = texto
        i.put()

    def obtener_comentarios(self):
        return Comentario.query(Comentario.id_receta == self.get_id()).order(-Comentario.date)


class Comentario(ndb.Model):

    texto = ndb.StringProperty()

    nick = ndb.StringProperty()

    id_receta = ndb.GenericProperty()

    date = ndb.DateTimeProperty(auto_now_add=True)

