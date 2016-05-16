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

from session_module import BaseSessionHandler

template_dir = os.path.join(os.path.dirname(__file__), 'Plantillas')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                               autoescape = True)


def render_str(template, **params):
    t = jinja_env.get_template(template)
    return t.render(params)


class Handler(BaseSessionHandler):
    def render(self, template, **kw):
        self.response.out.write(render_str(template, **kw))

    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)


class MainHandler(Handler):
    def get(self):
        usuario = self.session.get('username')
        rol = self.session.get('rol')
        login="no"
        if usuario:
            login = "si"
        if not rol:
            rol = "Anonimo"
        self.render("index.html", rol=rol, login=login)


class RecetaHandler(Handler):
    def get(self):
        usuario = self.session.get('username')
        rol = self.session.get('rol')
        login="no"
        if usuario:
            login = "si"
        if not rol:
            rol = "Anonimo"
        self.render("receta.html", rol=rol, login=login)


class RegistroHandler(Handler):
    def get(self):
        usuario = self.session.get('username')
        rol = self.session.get('rol')
        login="no"
        if usuario:
            login = "si"
        if not rol:
            rol = "Anonimo"
        self.render("registro.html", rol=rol, login=login)


class LoginHandler(Handler):
    def get(self):
        usuario = self.session.get('username')
        rol = self.session.get('rol')
        login="no"
        if usuario:
            login = "si"
        if not rol:
            rol = "Anonimo"
        self.render("login.html", rol=rol, login=login)


class CatalogoHandler(Handler):
    def get(self):
        usuario = self.session.get('username')
        rol = self.session.get('rol')
        login="no"
        if usuario:
            login = "si"
        if not rol:
            rol = "Anonimo"
        self.render("pcr.html", rol=rol, login=login)

config = {}
config['webapp2_extras.sessions'] = {
    'secret_key': 'my-super-secret-key',
}

app = webapp2.WSGIApplication([
    ('/receta', RecetaHandler), ('/', MainHandler), ('/registro', RegistroHandler), ('/login', LoginHandler),
    ('/catalogo', CatalogoHandler)
], config=config,debug=True)
