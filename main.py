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

from Estructuras.Usuarios import Usuario
from Estructuras.Recetas import Receta


class MainHandler(webapp2.RequestHandler):
    def get(self):

        p = Usuario.query(Usuario.nick == "javi")
        u = p.fetch()[0]
        r = Receta(id_usuario=u.key.id(),
                   id_categoria="2",
                   nombre="Flan",
                   etiquetas="prueba")
        r.put()

        self.response.write('Esto empieza a funcionar '+u.get_id_as_str())


app = webapp2.WSGIApplication([
    ('/', MainHandler)
], debug=True)
