import cherrypy
from morena.root import *
from morena.lib import *
from morena.session import *

config = {
    '/static': {
        'tools.staticdir.on': True,
        'tools.staticdir.dir': os.path.join(current_dir, 'media/public')
    },
    '/fotos': {
        'tools.staticdir.on': True,
        'tools.staticdir.dir': os.path.join(current_dir, 'media/fotos')
    },
    '/' : {
        'tools.sessions.on': True,
        'tools.sessions.storage_type': 'my'
    }
}

cherrypy.config.update({'engine.autoreload_on': False})
cherrypy.lib.sessions.MySession = MySession
app = cherrypy.tree.mount(root, '/', config=config)

def application(environ, start_response):
    return app(environ, start_response)