
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
import uuid
import hashlib

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
        self.render("logout.html",
                        rol='Anonimo',
                        login='no'
                        )

class Login(Handler):

    def get(self, username="", password="",username_error=""):

        if self.session.get('username'):
            self.render("errores.html",
                            rol='Usuario',
                            login='si',
                            message= self.session.get('username')+ ' ya estas logueado',
                            )
        else:
            self.write(render_str("login.html",rol='Anonimo', login='no') % {"username" :username,
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

        hash_object = hashlib.sha512(user_password)
        hex_dig = hash_object.hexdigest()

        user=Usuario.query(Usuario.nick==user_username and Usuario.password==hex_dig).get()
        if user:
            #Usuario encontrado
            if user.activado:
                #Usuario activado
                self.session['rol'] = user.rol
                self.session['username'] = sani_username
                self.render("index.html",
                                rol=user.rol,
                                login='si',
                             #   message = sani_username+' logueado correctamente',
                                )
            else:
                #Usuario sin activar
                self.write(render_str("login.html",rol='Anonimo', login='no') % {"username" :sani_username,
                "password" : "",
                "username_error" : "El usuario no esta activado"})

        else:
            #No se encontro al usuario
            self.write(render_str("login.html",rol='Anonimo', login='no') % {"username" :sani_username,
            "password" : "",
            "username_error" : "No existe dicha combinacion de usuario y password"})


class googleAuth(Handler):
    def post(self):
        usuarioGoogleId = self.request.get('usuarioGoogleId')
        usuarioGoogleName = self.request.get('usuarioGoogleName')
        usuarioGoogleEmail = self.request.get('usuarioGoogleEmail')


        #Si no existe el usuario, se registra en nuestra BBDD
        user=Usuario.query(Usuario.nick==usuarioGoogleName).count()
        if user==0:
            u=Usuario()
            u.nick=usuarioGoogleName
            u.email=usuarioGoogleEmail
            u.password = "googleAccount"
            u.name= usuarioGoogleName
            u.surname = ""
            u.activado = True
            u.rol = "Usuario"
            u.put()
            self.session['rol'] = "Usuario"
            self.session['username'] = usuarioGoogleName
            #Usuario activado
            self.response.out.write("usuario creado y  logueado")

        else:
            #usuario ya en la BBDD
            user=Usuario.query(Usuario.nick==usuarioGoogleName).get()
            self.session['rol'] = user.rol
            self.session['username'] = user.nick
            self.response.out.write("usuario logueado")



config = {}
config['webapp2_extras.sessions'] = {
    'secret_key': 'my-super-secret-key',
}
app = webapp2.WSGIApplication([
    ('/login', Login),
    ('/logout', Logout),
    ('/googleAuth', googleAuth)
    ],config=config, debug=True)
