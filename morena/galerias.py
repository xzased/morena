import cherrypy
from mongo import *
from document import *
from tools import *
from lib import *
from PIL import Image, ImageOps

class Galerias:

    @cherrypy.expose
    @cherrypy.tools.auth(level='mortal')
    def index(self, **params):
        page = int(params.get('pagina', 1))
        galerias = Mongo(Galeria).find()
        current_page = Page(galerias, page, '/org/galerias', 10)
        records = current_page.items()
        galerias = list()
        for record in records:
            fotos = Mongo(Foto).find({'galeria_id': str(record['_id'])})[0:3]
            galerias.append((record, fotos))
        tmpl = env.get_template('galerias.html')
        return tmpl.render(galerias=galerias, pager=current_page)

    @cherrypy.expose
    @cherrypy.tools.auth(level='mortal')
    def ver_galeria(self, **params):
        _id = params.get('oid')
        galeria = Mongo(Galeria).find_id(_id)
        fotos = Mongo(Foto).find({'galeria_id': _id})
        tmpl = env.get_template('ver_galeria.html')
        return tmpl.render(galeria=galeria, fotos=fotos)

    @cherrypy.expose
    @cherrypy.tools.auth(level='mortal')
    def agregar_galeria(self, **params):
        if cherrypy.request.method == 'POST':
            now = datetime.now()
            name = params.get('nombre')
            if Mongo(Galeria).find_one('nombre', name) or not name:
                raise HTTPError(500)
            user = cherrypy.session.get('user')
            params.update({'fecha': now, 'usuario': user})
            galeria = Galeria()
            galeria.update(params)
            galeria = Mongo(Galeria).add(galeria)
            return json.dumps(galeria, default=json_handler)
        tmpl = env.get_template('agregar_galeria.html')
        return tmpl.render()

    @cherrypy.expose
    @cherrypy.tools.auth(level='mortal')
    def borrar_galeria(self, galerias):
        if cherrypy.request.method == 'POST':
            galerias = json.loads(galerias)
            for galeria in galerias:
                g = Mongo(Galeria).find_id(galeria)
                fotos = Mongo(Foto).find({'galeria_id': galeria})
                for foto in fotos:
                    self.eraser(foto)
                Mongo(Galeria).remove(g)
            return json.dumps({'success': True})

    @cherrypy.expose
    def subir_foto(self, foto=None, **params):
        if cherrypy.request.method == 'POST':
            name = foto.filename.replace(" ", "-")
            if name in os.listdir(upload_path):
                name = name.split('.', 1)[0] + '-1.jpg'
            size = 0
            f = open(('%s/%s' % (upload_path, name)), 'a')
            while True:
                data = foto.file.read(8192)
                if not data:
                    break
                f.write(data)
                size += len(data)
            f.close()
            url = '%s/%s' % (upload_path, name)
            thumb = '%s/%s' % (thumbnail_path, name)
            big = Image.open(url)
            big.thumbnail((600, 600), Image.ANTIALIAS)
            big.save(url, 'JPEG')
            small = Image.open(url)
            centered = ImageOps.fit(small, (80, 80), Image.ANTIALIAS)
            centered.save(thumb, 'JPEG')
            params.update({'url': '/static/fotos/%s' % name,
                    'thumb-url': '/static/fotos/thumbs/%s' % name, 'fecha': datetime.now()})
            pic = Foto()
            pic.update(params)
            pic = Mongo(Foto).add(pic)
            return json.dumps(pic, default=json_handler)
        galerias = Mongo(Galeria).find()
        tmpl = env.get_template('subir_foto.html')
        return tmpl.render(galerias=galerias)

    @cherrypy.expose
    def borrar_foto(self, oid):
        if cherrypy.request.method == 'POST':
            f = Mongo(Foto).find_id(oid)
            if self.eraser(f):
                return json.dumps({'success': True})

    def eraser(self, f):
        filename = f['url'].split('/')[-1]
        os.remove('%s/%s' % (upload_path, filename))
        os.remove('%s/%s' % (thumbnail_path, filename))
        Mongo(Foto).remove(f)
        return True