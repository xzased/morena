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

cherrypy.lib.sessions.MySession = MySession

cherrypy.tree.mount(root, '/', config=config)
cherrypy.engine.start()
cherrypy.engine.block()
