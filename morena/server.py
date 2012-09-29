import cherrypy
import os
from pages import *
from session import MySession

current_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

config = {
    '/static': {
        'tools.staticdir.on': True,
        'tools.staticdir.dir': os.path.join(current_dir, 'static')
    }
}

config_app = {
    '/static': {
        'tools.staticdir.on': True,
        'tools.staticdir.dir': os.path.join(current_dir, 'static')
    },
    '/' : {
        'tools.sessions.on': True,
        'tools.sessions.storage_type': 'my'
    }
}

cherrypy.lib.sessions.MySession = MySession

cherrypy.tree.mount(Root(), '/', config=config)
cherrypy.tree.mount(App(), '/org', config=config_app)
cherrypy.engine.start()
cherrypy.engine.block()