import cherrypy
import json
from datetime import datetime
from mongo import *
from document import *
from tools import *
from lib import *
from session import *

cherrypy.lib.sessions.MySession = MySession

class Org:

    @cherrypy.expose
    def index(self):
        if cherrypy.session.get('wop', None):
            raise cherrypy.HTTPRedirect("/org/articulos")
        tmpl = env.get_template('login.html')
        return tmpl.render()

    @cherrypy.expose
    def login(self, **params):
        if cherrypy.request.method == 'POST':
            user = Mongo(User).find_one('username', params.get('user'))
            passwd = params.get('passwd')
            if not user or not user.check_password(passwd):
                raise cherrypy.HTTPError(401)
            wop = set_random_session()
            active = ActiveSession()
            active['user'] = params.get('user')
            active['wop'] = wop
            Mongo(ActiveSession).add(active)
            cherrypy.session['wop'] = wop
            raise cherrypy.HTTPRedirect("/org/articulos")
        return cherrypy.HTTPError(404)

    @cherrypy.expose
    def logout(self, **params):
        if cherrypy.request.method == 'POST':
            cherrypy.lib.sessions.expire()
            raise cherrypy.HTTPRedirect('/')
        return cherrypy.HTTPError(404)