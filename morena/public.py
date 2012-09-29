import cherrypy
import json
from datetime import datetime
from mongo import *
from document import *
from tools import *
from lib import *

class Public:

    @cherrypy.expose
    def index(self):
        todos = Mongo(Articulo).find()
        articulos = todos[0:4]
        otros = todos[4:8]
        tmpl = env.get_template('index.html')
        return tmpl.render(articulos=articulos, otros=otros)

    @cherrypy.expose
    def editorial(self, **params):
        todos = Mongo(Articulo).find({'categoria': 'editorial'})
        page = int(params.get('pagina', 1))
        current_page = Page(todos, page, '/editorial', 10)
        articulos = current_page.items()
        tmpl = env.get_template('editorial.html')
        return tmpl.render(articulos=articulos, pager=current_page)

    @cherrypy.expose
    def participa(self, **params):
        todos = Mongo(Articulo).find({'categoria': 'participa'})
        page = int(params.get('pagina', 1))
        current_page = Page(todos, page, '/participa', 10)
        articulos = current_page.items()
        tmpl = env.get_template('participa.html')
        return tmpl.render(articulos=articulos, pager=current_page)

    @cherrypy.expose
    def contacto(self, **params):
        todos = Mongo(Articulo).find({'categoria': 'contacto'})
        page = int(params.get('pagina', 1))
        current_page = Page(todos, page, '/contacto', 10)
        articulos = current_page.items()
        tmpl = env.get_template('contacto.html')
        return tmpl.render(articulos=articulos, pager=current_page)

    @cherrypy.expose
    def eventos(self, **params):
        todos = Mongo(Articulo).find({'categoria': 'eventos'})
        page = int(params.get('pagina', 1))
        current_page = Page(todos, page, '/eventos', 10)
        articulos = current_page.items()
        tmpl = env.get_template('eventos.html')
        return tmpl.render(articulos=articulos, pager=current_page)

    @cherrypy.expose
    def galeria(self, **params):
        page = int(params.get('pagina', 1))
        galerias = Mongo(Galeria).find()
        current_page = Page(galerias, page, '/org/galerias', 10)
        records = current_page.items()
        galerias = list()
        for record in records:
            fotos = Mongo(Foto).find({'galeria_id': str(record['_id'])})[0:3]
            galerias.append((record, fotos))
        tmpl = env.get_template('galeria.html')
        return tmpl.render(galerias=galerias, pager=current_page)

    @cherrypy.expose
    def ver_galeria(self, **params):
        _id = params.get('oid')
        galeria = Mongo(Galeria).find_id(_id)
        fotos = Mongo(Foto).find({'galeria_id': _id})
        tmpl = env.get_template('ver_galeria_mortal.html')
        return tmpl.render(galeria=galeria, fotos=fotos)