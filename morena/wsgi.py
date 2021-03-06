import cherrypy
from root import *
from lib import *
from session import *

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
        'tools.sessions.storage_type': 'my',
        'engine.autoreload_on': False
    }
}

cherrypy.server.unsubscribe()
cherrypy.lib.sessions.MySession = MySession
application = cherrypy.tree.mount(root, '/', config=config)
