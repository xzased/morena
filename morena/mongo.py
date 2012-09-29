from pymongo import Connection
from bson.objectid import ObjectId

try:
    default_connection = Connection('localhost', 27017)
except:
    raise Exception("Could not connect to mongo.")

default_connection = Connection()

class Mongo(object):
    def __init__(self, doc, connection=default_connection):
        self.connection = connection
        self.db = self.connection[doc.__db__]
        self.collection = self.db[doc.__collection__]
        self._doc = doc

    def add(self, document):
        doc = self._sanitize(document)
        oid = self.collection.insert(doc)
        return self.find_id(oid)

    def remove(self, document):
        self.collection.remove({'_id': ObjectId(document['_id'])})

    def update(self, document):
        oid = document.pop('_id')
        doc = self._sanitize(document)
        self.collection.update({'_id': ObjectId(oid)}, doc, upsert=False)
        return self.find_id(oid)

    def save(self, document):
        doc = self._sanitize(document)
        print doc
        oid = self.collection.save(doc, safe=True)
        return self.find_id(oid)

    def find_one(self, key, val):
        ret = self.collection.find_one({key:val})
        if ret:
            doc = self._set_values(ret)
            return doc
        else:
            return ret

    def find_id(self, val):
        ret = self.collection.find_one({'_id': ObjectId(val)})
        if ret:
            doc = self._set_values(ret)
            return doc
        else:
            return ret

    def find(self, params=dict()):
        ret = self.collection.find(params)
        docs = [self._set_values(i) for i in ret if i is not None]
        return docs

    def count(self):
        ret = self.collection.count()
        return ret

    def _set_values(self, document):
        new = self._doc()
        for k, v in document.items():
            new[k] = v
        return new

    def _sanitize(self, document):
        for k, v in document.items():
            if not k in self._doc.__valid__:
                del document[k]
        return document