
import webapp2
import os
import jinja2
import re
import cgi
import session_module
from BaseHandler import BaseHandler
from webapp2_extras import sessions
from Estructuras.Usuarios import Usuario
from google.appengine.ext import db

template_dir = os.path.join(os.path.dirname(__file__), 'Plantillas')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                               autoescape = True)


def render_str(template, **params):
    t = jinja_env.get_template(template)
    return t.render(params)


class Handler(BaseHandler):
    def render(self, template, **kw):
        self.response.out.write(render_str(template, **kw))
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

class Logout(Handler):
    def get(self):
        for k in self.session.keys():
            del self.session[k]
        self.render("errores.html",
                        rol='Usuario',
                        login='no',
                        message= 'Hasta pronto',
                        )

class Login(Handler):

    def get(self, username="", password="",username_error=""):

        if self.session.get('username'):
            self.render("errores.html",
                            rol='Usuario',
                            login='no',
                            message= self.session.get('username')+ ' ya estas logueado',
                            )
        else:
            self.write(render_str("login.html") % {"username" :username,
                "password" : password,
                "username_error" : username_error}
                )

    def post(self):
        def escape_html(s):
            return cgi.escape(s, quote=True)

        user_username = self.request.get('username')
        user_password = self.request.get('password')
        sani_username = escape_html(user_username)
        sani_password = escape_html(user_password)

        user=Usuario.query(Usuario.nick==user_username and Usuario.password==user_password).get()
        if user:
            if user.activado:
                #Usuario sin activar
                self.write(render_str("login.html") % {"username" :sani_username,
                "password" : "",
                "username_error" : "El usuario no esta activado"})
            else:
                #Usuario encontrado, loguearlo
                #env.globals['username'] = sani_username # Your session
                self.session['rol'] = user.rol
                self.session['username'] = sani_username
                self.render("errores.html",
                                rol='Usuario',
                                login='no',
                                message = sani_username+' logueado correctamente',
                                )
        else:
            #No se encontro al usuario
            self.write(render_str("login.html") % {"username" :sani_username,
            "password" : "",
            "username_error" : "No existe dicha combinacion de usuario y password"})




config = {}
config['webapp2_extras.sessions'] = {
    'secret_key': 'my-super-secret-key',
}
app = webapp2.WSGIApplication([
    ('/login', Login),
    ('/logout', Logout)
    ],config=config, debug=True)