
import webapp2
import os
import jinja2
import re
import cgi
from BaseHandler import BaseHandler

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


signup_form='''<html>
<head>
    <link type="text/css" rel="stylesheet" href="/stylesheets/main.css" />
    <title>Introduzca sus datos:</title>
    <style type="text/css"> .label {text-align: right} .error {color: red} </style>
</head>
<body>
<form method="post">
<table>
    <tr>
        <td class="label"> Nombre de usuario </td>
        <td> <input type="text" name="username" value="%(username)s" placeholder="Tu nombre..."> </td>
        <td class="error"> %(username_error)s </td>
    </tr>
    <tr>
        <td class="label"> Password</td>
        <td> <input type="password" name="password"value="%(password)s" autocomplete="off"> </td>
        <td class="error"> %(password_error)s </td>
    </tr>
    <tr>
        <td class="label"> Repetir Password </td>
        <td> <input type="password" name="verify" value="%(verify)s" placeholder="El mismo de antes">
        </td> <td class="error"> %(verify_error)s </td>
    </tr>
    <tr>
        <td class="label">Email </td>
        <td> <input type="text" name="email" value="%(email)s"> </td>
        <td class="error">%(email_error)s </td>
    </tr>
</table>
<input type="submit">
</form>
</body>
</html>'''


class Register(Handler):

    def get(self, username="", password="", verify="",email="", username_error="", password_error="",verify_error="", email_error="",name="",surname="",name_error="",surname_error=""):
        #self.write_form()
        #self.render_str("registro.html")

        self.write(render_str("registro.html") % {"username" :username,
        "password" : password,
        "verify" : verify,
        "email" : email,
        "name" : name,
        "surname" : surname,
        "username_error" : username_error,
        "password_error" : password_error,
        "verify_error" : verify_error,
        "email_error" : email_error,
        "name_error" : name_error,
        "surname_error" : surname_error}
        )

    def post(self):
        def escape_html(s):
            return cgi.escape(s, quote=True)

        USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
        PASSWORD_RE = re.compile(r"^.{3,20}$")
        EMAIL_RE = re.compile(r"^[\S]+@[\S]+\.[\S]+$")
        NOMBRE_RE = re.compile(r"^[a-zA-Z-]{3,30}$")
        def valid_username(username):
            return USER_RE.match(username)
        def valid_password(password):
            return PASSWORD_RE.match(password)
        def valid_email(email):
            return EMAIL_RE.match(email)
        def valid_name(nombre):
            return NOMBRE_RE.match(nombre)

        user_username = self.request.get('username')
        user_password = self.request.get('password')
        user_verify = self.request.get('verify')
        user_email = self.request.get('email')
        user_name = self.request.get('name')
        user_surname = self.request.get('surname')
        sani_username = escape_html(user_username)
        sani_password = escape_html(user_password)
        sani_verify = escape_html(user_verify)
        sani_email = escape_html(user_email)
        sani_name = escape_html(user_name)
        sani_surname = escape_html(user_surname)
        username_error = ""
        password_error = ""
        verify_error = ""
        email_error = ""
        name_error = ""
        surname_error = ""

        error = False
        if not valid_username(user_username):
            username_error = "Nombre incorrecto!: "+self.request.get('username')
            error = True
        if not valid_password(user_password):
            password_error = "Password incorrecto!"
            error = True
        if not user_verify or not user_password == user_verify:
            verify_error = "Password no coincide!"
            error = True
        if not valid_email(user_email):
            email_error = "Email incorrecto!"
            error = True
        if not valid_name(user_name):
            email_error = "Nombre incorrecto!"
            error = True
        if not valid_name(user_surname):
            email_error = "Apellido incorrecto!"
            error = True


        if error:
            self.write(render_str("registro.html") % {"username" :sani_username,
            "password" : sani_password,
            "verify" : sani_verify,
            "email" : sani_email,
            "name" : sani_name,
            "surname" : sani_surname,
            "username_error" : username_error,
            "password_error" : password_error,
            "verify_error" : verify_error,
            "email_error" : email_error,
            "name_error" : name_error,
            "surname_error" : surname_error})
        else:
            user=Usuario.query(Usuario.nick==user_username).count()
            if user==0:
                u=Usuario()
                u.nick=user_username
                u.email=user_email
                u.password=user_password
                u.name= user_name
                u.surname = user_surname
                u.rol = "Usuario"
                u.put()
                self.render("errores.html",
                                rol='Usuario',
                                login='no',
                                message='Usuario creado correctamente',
                                )
            else:
                self.write(render_str("registro.html") % {"username" :sani_username,
                "password" : sani_password,
                "verify" : sani_verify,
                "email" : sani_email,
                "name" : name,
                "surname" : surname,
                "username_error" : "Nick actualmente en uso",
                "password_error" : password_error,
                "verify_error" : verify_error,
                "email_error" : email_error,
                "name_error" : name_error,
                "surname_error" : surname_error})




config = {}
config['webapp2_extras.sessions'] = {
    'secret_key': 'my-super-secret-key',
}
app = webapp2.WSGIApplication([
    ('/registro', Register)
    ],config=config, debug=True)
