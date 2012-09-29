import cherrypy
from mongo import *
from document import *
from tools import *
from lib import *

class Usuarios:

    @cherrypy.expose
    @cherrypy.tools.auth(level='admin')
    def usuarios(self, **params):
        usuarios = Mongo(User).find()
        tmpl = env.get_template('usuarios.html')
        return tmpl.render(usuarios=usuarios)

    @cherrypy.expose
    @cherrypy.tools.auth(level='admin')
    def agregar_usuario(self, **params):
        if cherrypy.request.method == 'POST':
            user = params.get('user')
            passwd = params.get('passwd')
        if 'oid' in params.keys():
            user = Mongo(User).find_id(params.get('oid'))
        else:
            user = None
        comisiones = Mongo(Comision).find()
        niveles = Mongo(Nivel).find()
        tmpl = env.get_template('agregar_usuario.html')
        return tmpl.render(comisiones=comisiones, niveles=niveles, user=user)