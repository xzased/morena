from mongo import *
import random
import hashlib

class Document(dict):
    __db__ = 'morena'

    def __setitem__(self, key, value):
        if not key in self.__valid__:
            raise KeyError("%s is not a valid key." % key)
        else:
            dict.__setitem__(self, key, value)

class ActiveSession(Document):
    __collection__ = 'sessions'
    __valid__ = ['_id', 'wop', 'user']

class User(Document):
    __collection__ = 'users'
    __valid__ = ['_id', 'username', 'password', 'nombre',
                    'apellido', 'comision', 'nivel', 'foto']

    def set_password(self, raw_password):
        salt = hashlib.sha1('%s$@$%s' % (str(random.random()), str(random.random()))).hexdigest()[:5]
        hsh = hashlib.sha1('%s$@$%s' % (salt, raw_password)).hexdigest()
        self['password'] = '%s$@$%s' % (salt, hsh)

    def check_password(self, raw_password):
        salt, hsh = self['password'].split('$@$')
        return hsh == hashlib.sha1('%s$@$%s' % (salt, raw_password)).hexdigest()

class Nivel(Document):
    __collection__ = 'niveles'
    __valid__ = ['_id', 'nivel', 'descripcion']

class Comision(Document):
    __collection__ = 'comision'
    __valid__ = ['_id', 'comision', 'descripcion']

class Categoria(Document):
    __collection__ = 'categoria'
    __valid__ = ['_id', 'categoria']

class Articulo(Document):
    __collection__ = 'articulo'
    __valid__ = ['_id', 'categoria', 'titulo', 'contenido', 'documentos', 'orden', 'fecha', 'usuario']

class Portada(Document):
    __collection__ = 'portada'
    __valid__ = ['_id', 'titulo', 'foto', 'link', 'descripcion', 'orden', 'fecha', 'usuario']

class Galeria(Document):
    __collection__ = 'galeria'
    __valid__ = ['_id', 'nombre', 'descripcion', 'fecha', 'usuario', 'orden']

class Foto(Document):
    __collection__ = 'fotos'
    __valid__ = ['_id', 'galeria_id', 'fecha', 'usuario', 'titulo', 'url', 'thumb-url', 'descripcion', 'orden']