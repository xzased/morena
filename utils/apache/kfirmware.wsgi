from kfirmware.root import *
import cherrypy

cherrypy.config.update(config)
cherrypy.config.update({'environment': 'embedded'})

application = cherrypy.Application(root, script_name=None, config=None)