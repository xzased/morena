from cherrypy.lib import sessions
from cherrypy._cpcompat import copyitems
from document import ActiveSession
from mongo import *

class MySession(sessions.RamSession):
    def clean_up(self):
        """Clean up expired sessions."""
        now = self.now()
        for id, (data, expiration_time) in copyitems(self.cache):
            if expiration_time <= now:
                try:
                    active = Mongo(ActiveSession).find_one('wop', self.cache['wop'])
                    Mongo(ActiveSession).remove(active)
                except:
                    print "Failed to remove active session object."
                try:
                    del self.cache[id]
                except KeyError:
                    pass
                try:
                    del self.locks[id]
                except KeyError:
                    pass
        # added to remove obsolete lock objects
        for id in list(self.locks):
            if id not in self.cache:
                self.locks.pop(id, None)
