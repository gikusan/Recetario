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
from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers


template_dir = os.path.join(os.path.dirname(__file__), 'Plantillas')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                               autoescape = True)


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
        rol = "Usuario"
        if rol=="Anonimo":
            self.write("No tienes permiso")
        else:
            self.render_upload("recetaformulario.html",
                               rol='Usuario',
                               login='no'
                               )

class MainHandler(Handler):
    def get(self):

        receta_key = self.request.get('id')

        if not receta_key:
            self.error(404)
            self.response.write("Receta no encontrada")
        else:
            r = Receta.get_by_id(int(receta_key))

            self.render("receta.html",
                        rol='Anonimo',
                        login='no',
                        receta=r,
                        id = r.get_id(),
                        Ingredientes=r.obtener_ingredientes(),
                        Pasos=r.obtener_pasos())

class ErrorHandler(Handler):
    def get(self):
        self.render("errores.html",
                        rol='Usuario',
                        login='no',
                        message='Problemas con la subida de imagen o el titulo',
                        )

class PhotoUploadHandler(blobstore_handlers.BlobstoreUploadHandler):
    def post(self):
        try:
            upload_files = self.get_uploads('file')
            blob_info = upload_files[0]

            r = Receta(
                nombre=self.request.get("nombre"),
                descripcion = self.request.get("descripcion"),
                etiquetas = self.request.get("tags"),
                id_categoria = self.request.get("categoria"),
                blob_key= blob_info.key()
            )

            r.put()


            self.redirect('/receta/editar?id=%s' % r.get_id())

        except:
            self.redirect('/receta/error')

class EditHandler(Handler):
    def get(self):

        receta_key = self.request.get('id')

        if not receta_key:
            self.error(404)
            self.response.write("Receta no encontrada")
        else:
            r = Receta.get_by_id(int(receta_key))

            self.render("receta.html",
                        rol='Anonimo',
                        login='no',
                        receta=r,
                        id = r.get_id(),
                        Ingredientes=r.obtener_ingredientes(),
                        Pasos=r.obtener_pasos())
config = {}
config['webapp2_extras.sessions'] = {
    'secret_key': 'my-super-secret-key',
}
app = webapp2.WSGIApplication([
    ('/receta/ver', MainHandler),
    ('/receta/crear', RegisterHandler),
    ('/receta/crear2', PhotoUploadHandler),
    ('/receta/editar', EditHandler),
    ('/receta/error', ErrorHandler)
],config=config, debug=True)

