import cherrypy
from mongo import *
from document import *
from tools import *
from lib import *

class Articulos:

    @cherrypy.expose
    @cherrypy.tools.auth(level='mortal')
    def index(self, **params):
        page = int(params.get('pagina', 1))
        articulos = Mongo(Articulo).find()
        current_page = Page(articulos, page, '/org/articulos', 10)
        records = current_page.items()
        tmpl = env.get_template('articulos.html')
        return tmpl.render(articulos=records, pager=current_page)

    @cherrypy.expose
    @cherrypy.tools.auth(level='admin')
    def agregar_articulo(self, **params):
        if cherrypy.request.method == 'POST':
            now = datetime.now()
            user = cherrypy.session.get('user')
            params.update({'fecha': now, 'usuario': user})
            articulo = Articulo()
            articulo.update(params)
            articulo = Mongo(Articulo).add(articulo)
            return json.dumps(articulo, default=json_handler)
        categorias = Mongo(Categoria).find()
        tmpl = env.get_template('agregar_articulo.html')
        return tmpl.render(categorias=categorias)

    @cherrypy.expose
    @cherrypy.tools.auth(level='mortal')
    def borrar_articulo(self, **params):
        if cherrypy.request.method == 'POST':
            error = list()
            articulos = json.loads(params.get('articulos'))
            for articulo in articulos:
                try:
                    adios = Mongo(Articulo).find_id(articulo)
                    Mongo(Articulo).remove(adios)
                except:
                    error.append(articulo)
            return json.dumps({'error': error})
        raise cherrypy.HTTPError(404)

    @cherrypy.expose
    @cherrypy.tools.auth(level='mortal')
    def modificar_articulo(self, **params):
        if cherrypy.request.method == 'POST':
            mod = params.get('articulo')
            articulo = Mongo(Articulo).find_id(mod)
            categorias = Mongo(Categoria).find()
            tmpl = env.get_template('modificar_articulo.html')
            return tmpl.render(articulo=articulo, categorias=categorias)

    @cherrypy.expose
    @cherrypy.tools.auth(level='mortal')
    def guardar_articulo(self, **params):
        if cherrypy.request.method == 'POST':
            now = datetime.now()
            user = cherrypy.session.get('user')
            params.update({'fecha': now, 'usuario': user})
            articulo = Mongo(Articulo).find_id(params.get('_id'))
            articulo.update(params)
            articulo = Mongo(Articulo).update(articulo)
            return json.dumps(articulo, default=json_handler)