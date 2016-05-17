#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
import os
import jinja2

from Estructuras.Recetas import Receta
from BaseHandler import BaseHandler
from Estructuras.Usuarios import Usuario
from Estructuras.Ingredientes import Ingrediente
from Estructuras.Pasos import Paso

from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers
from google.appengine.ext import ndb


template_dir = os.path.join(os.path.dirname(__file__), 'Plantillas')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                               autoescape = True)

"""
    Funcion para coincidencias
"""


def buscar_contenido(parametro1, parametro2, parametro3, busqueda):
    if busqueda in parametro1:
        return True
    elif busqueda in parametro2:
        return True
    elif busqueda in parametro3:
        return True
    else:
        return False


"""
    Funcion para buscar
"""


def buscar_recetas(busqueda):
    resultado = []
    recetas = Receta.query().fetch()
    for r in recetas:
        if buscar_contenido(r.id_categoria, r.etiquetas, r.nombre, busqueda):
            print(r.nombre)
            resultado.append(r)
    return resultado


def render_str(template, **params):
    t = jinja_env.get_template(template)
    return t.render(params)




class Handler(BaseHandler):
    def render(self, template, **kw):
        self.response.out.write(render_str(template, **kw))

    def render_upload(self, template, **kw):
        upload_url = blobstore.create_upload_url('/receta/crear2')
        self.response.out.write(render_str(template, **kw) % {'url': upload_url})

    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)


class RegisterHandler(Handler):
    def get(self):
        rol = self.session.get('rol')
        if not rol:
            rol = "Anonimo"
        if rol == "Anonimo":
            self.write("No tienes permiso")
        else:
            self.render_upload("recetaformulario.html",
                               rol=rol,
                               login='si'
                               )


class AddInstructionHandler(Handler):
    def post(self):
        try:
            receta_key = self.request.get('id')
            nombre = self.request.get('nombre')
            cantidad = self.request.get('cantidad')
            descripcion = self.request.get('descripcion')

            if nombre != "" and cantidad != " ":
                r = Receta.get_by_id(int(receta_key))
                if r:
                    r.insertar_ingrediente(nombre, cantidad, descripcion)
                    self.write("OK")
                else:
                    self.write("ERROR")
            else:
                self.write("ERROR")
        except ValueError:
            self.write(ValueError)


class RemoveInstructionHandler(Handler):
    def post(self):
        try:

            ingrediente_key = self.request.get('id')
            i = Ingrediente.get_by_id(int(ingrediente_key))
            if i:
                i.delete()
                self.write("OK")
            else:
                self.write("ERROR")

        except ValueError:
            self.write(ValueError)


class AddPasoHandler(Handler):
    def post(self):
        try:
            receta_key = self.request.get('id')
            tiempo = int(self.request.get('tiempo'))
            descripcion = self.request.get('descripcion')

            if descripcion != "" and tiempo > 0:
                r = Receta.get_by_id(int(receta_key))
                if r:
                    r.insertar_paso(descripcion, tiempo)
                    self.write("OK")
                else:
                    self.write("ERROR")
            else:
                self.write("ERROR")

        except ValueError:
            self.write(ValueError)


class RemovePasoHandler(Handler):
    def post(self):
        try:
            paso_key = self.request.get('id')
            p = Paso.get_by_id(int(paso_key))
            if p:
                p.delete()
                self.write("OK")
            else:
                self.write("ERROR")

        except ValueError:
            self.write(ValueError)


class MainHandler(Handler):
    def get(self):
        usuario = self.session.get('username')
        rol = self.session.get('rol')
        login = "no"
        receta_key = self.request.get('id')

        if not rol:
            rol = "Anonimo"
        if usuario:
            login = "si"

        if not receta_key:
            self.error(404)
            self.response.write("Receta no encontrada")
        else:
            r = Receta.get_by_id(int(receta_key))
            if r:
                self.render("receta.html",
                            rol=rol,
                            login=login,
                            receta=r,
                            editar='false',
                            id=r.get_id(),
                            Ingredientes=r.obtener_ingredientes(),
                            Pasos=r.obtener_pasos())
            else:
                self.response.write("Receta no encontrada")


class ErrorHandler(Handler):
    def get(self):

        usuario = self.session.get('username')
        rol = self.session.get('rol')
        if not rol:
            rol = "Anonimo"
        if usuario:
            login = "si"
        self.render("errores.html",
                    rol=rol,
                    login=login,
                    message='Problemas con la subida de imagen o el titulo',
                    )


class PhotoUploadHandler(blobstore_handlers.BlobstoreUploadHandler):
    def post(self):
        try:

            upload_files = self.get_uploads('file')
            blob_info = upload_files[0]
            r = Receta(
                nombre=self.request.get("nombre"),
                num_pasos=0,
                descripcion=self.request.get("descripcion"),
                etiquetas=self.request.get("tags"),
                id_categoria=self.request.get("categoria"),
                blob_key=blob_info.key()
            )

            r.put()

            self.redirect('/receta/editar?id=%s' % r.get_id())

        except ValueError:
            self.write(ValueError)


class EditHandler(Handler):
    def get(self):
        usuario = self.session.get('username')
        rol = self.session.get('rol')
        if usuario:

            u = Usuario.query(Usuario.nick == usuario).fetch()[0]

            receta_key = self.request.get('id')

            if not receta_key:
                self.error(404)
                self.response.write("Receta no encontrada")
            else:
                r = Receta.get_by_id(int(receta_key))
                if not r.id_usuario:
                    r.id_usuario = u.get_id()
                    r.put()
                elif r.id_usuario!=u.get_id :
                        self.render("errores.html",
                            rol=rol,
                            login="si",
                            message='No puedes editar recetas que no te pertenezcan',
                            )
                else:
                    self.render("receta.html",
                                rol='Anonimo',
                                login='no',
                                receta=r,
                                editar='true',
                                id = r.get_id(),
                                Ingredientes=r.obtener_ingredientes(),
                                Pasos=r.obtener_pasos())
        else:
            self.redirect("/")

class RecetasAllHandler(Handler):
    def get(self):
        login = "no"
        usuario = self.session.get('username')
        rol = self.session.get('rol')
        if usuario:
            login = "si"
        if not rol:
            rol = "Anonimo"
        recetas = Receta.query().fetch()
        self.render("pcr.html", rol=rol, login=login, recetas=recetas)


class RecetasPropiasHandler(Handler):
    def get(self):
        login = "no"
        usuario = self.session.get('username')
        rol = self.session.get('rol')
        if usuario:
            login = "si"

        u = Usuario.query(Usuario.nick == usuario).fetch()[0]

        recetas = Receta.query(Receta.id_usuario==u.get_id()).fetch()

        self.render("pcr.html", rol=rol, login=login, recetas=recetas)


class RecetasCategoriaHandler(Handler):
    def get(self):
        login = "no"
        usuario = self.session.get('username')
        rol = self.session.get('rol')

        if usuario:
            login = "si"
        if not rol:
            rol ="Anonimo"

        categoria = self.request.get('categoria')
        recetas = buscar_recetas(categoria)

        self.render("pcr.html", rol=rol, login=login, recetas=recetas)


class BusquedaHandler(Handler):
    def get(self):
        login = "no"
        usuario = self.session.get('username')
        rol = self.session.get('rol')
        if usuario:
            login = "si"
        if not rol:
            rol = "Anonimo"
        recetas=[]
        self.render("pcrBusqueda.html", rol=rol, login=login, recetas=recetas)

    def post(self):

        buscar = self.request.get('buscar')

        print("este es el buscar :"+buscar)
        if buscar:
            recetas = buscar_recetas(buscar)
        else:
            recetas = []

        respuesta = ""
        receta_card = '''<div class="col s12 m4 l3">
                            <div class="card">
                                <div class="card-image waves-effect waves-block waves-light">
                                    <img class="activator" src="/view_photo?id=%(id)s">
                                </div>
                                <div class="card-content">
                                    <span class="card-title activator grey-text text-darken-4">%(nombre)s<i class="material-icons right">more_vert</i></span>
                                    <p><a href="/receta/ver?id={{r.get_id()}}">Ver Receta</a></p>
                                </div>
                                <div class="card-reveal">
                                    <span class="card-title grey-text text-darken-4">%(nombre)s<i class="material-icons right">close</i></span>
                                    <p class="truncate">%(descripcion)s</p>
                                    <br/>
                                </div>
                            </div>
                        </div> '''

        for r in recetas:
            respuesta += receta_card % {"id": r.get_id(),"nombre" :r.nombre,"descripcion" : r.descripcion}

        self.response.out.write(respuesta)



config = {}
config['webapp2_extras.sessions'] = {
    'secret_key': 'my-super-secret-key',
}
app = webapp2.WSGIApplication([
    ('/receta/ver', MainHandler),
    ('/receta/crear', RegisterHandler),
    ('/receta/crear2', PhotoUploadHandler),
    ('/receta/editar', EditHandler),
    ('/receta/error', ErrorHandler),
    ('/receta/addIns', AddInstructionHandler),
    ('/receta/delIns', RemoveInstructionHandler),
    ('/receta/addPas', AddPasoHandler),
    ('/receta/lista', RecetasAllHandler),
    ('/receta/delPas', RemovePasoHandler),
    ('/receta/propias', RecetasPropiasHandler),
    ('/receta/categoria', RecetasCategoriaHandler),
    ('/receta/busqueda', BusquedaHandler)
], config=config, debug=True)
