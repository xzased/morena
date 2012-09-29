import cherrypy
from document import ActiveSession
from mongo import Mongo
from document import User, ActiveSession

def auth(level='mortal'):
    session = cherrypy.session.get('wop')
    active = Mongo(ActiveSession).find_one('wop', session)
    if not session or not active:
        #raise cherrypy.HTTPError(404)
        raise cherrypy.HTTPRedirect("http://www.youtube.com/watch?v=qCVQpcY1au4")
    user = active.get('user', None)
    levels = Mongo(User).find_one('username', user).get('nivel', None)
    print levels
    if not levels or level not in levels:
        raise cherrypy.HTTPRedirect("http://www.youtube.com/watch?v=qCVQpcY1au4")
