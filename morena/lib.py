import cherrypy
import json
import os
import random
import hashlib
from tools import *
from datetime import datetime
from itertools import chain
from jinja2 import Environment, FileSystemLoader
from bson.objectid import ObjectId

current_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
env = Environment(loader=FileSystemLoader(os.path.join(current_dir, 'media/templates')))
cherrypy.tools.auth = cherrypy.Tool('before_handler', auth)
upload_path = os.path.join(current_dir, 'media/fotos')
thumbnail_path = os.path.join(current_dir, 'media/fotos/thumbs')

def json_handler(obj):
    if isinstance(obj, datetime):
        return obj.isoformat()
    elif isinstance(obj, ObjectId):
        return str(obj)
    else:
        return None

def set_random_session():
    salt = hashlib.sha1('%s$&$%s' % (str(random.random()), str(random.random()))).hexdigest()[:5]
    now = datetime.now().isoformat()
    hsh = hashlib.sha1('%s$&$%s' % (salt, now)).hexdigest()
    return '%s$&$%s' % (salt, hsh)

class Page(object):
    def __init__(self, collection, current_page, url, items_per_page=15):
        self.collection = collection
        self.current_page = current_page
        self.items_per_page = items_per_page
        self.url = url
        self._set_collection()

    def _process_collection(self):
        paginated = list()
        ln = len(self.collection)
        for start in range(0, ln, self.items_per_page):
            end = start + self.items_per_page
            if end > ln:
                end = ln
            paginated.append(self.collection[start:end])
        return paginated

    def _set_collection(self):
        self.paginated = self._process_collection()
        self.pages = len(self.paginated)

    def items(self):
        try:
            page = self.paginated[self.current_page - 1]
        except IndexError:
            page = list()
        return page

    def pager(self):
        html = str()
        for item in range(1, self.pages + 1):
            if item == self.current_page:
                tag = '<span class="pager_curpage">%i</span>' % item
            else:
                tag = '<a href="%s?pagina=%i" class="pager_link">%i</a>' \
                        % (self.url, item, item)
            html = html + tag
        return html
