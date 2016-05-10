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


from google.appengine.ext import db

template_dir = os.path.join(os.path.dirname(__file__), 'Plantillas')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                               autoescape = True)


def render_str(template, **params):
    t = jinja_env.get_template(template)
    return t.render(params)


class Handler(webapp2.RequestHandler):
    def render(self, template, **kw):
        self.response.out.write(render_str(template, **kw))

    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)


class MainHandler(Handler):
    def get(self):

        r = Receta.get_by_id(5752644836524032)
        self.render("receta.html",
                    rol='Anonimo',
                    login='no',
                    receta=r,
                    Ingredientes=r.obtener_ingredientes(),
                    Pasos=r.obtener_pasos())


app = webapp2.WSGIApplication([
    ('/receta', MainHandler)
], debug=True)

