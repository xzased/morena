#!/usr/bin/python
"""
Checks for required packages and pre-populates the database (Note: It will drop existig db)
"""
from morena.document import *
from morena.mongo import *
from morena.lib import *
from datetime import datetime

# Drop db
print "Dropping database 'morena' ...\n"
default_connection.drop_database('morena')

# Initialize data
print "Initializing data\n"

mortal = Nivel()
mortal.update({'nivel': 'mortal', 'descripcion': 'Meramente un usuario mortal'})
Mongo(Nivel).add(mortal)

comision = Nivel()
comision.update({'nivel': 'comision', 'descripcion': 'Para que no digan que no'})
Mongo(Nivel).add(mortal)

admin = Nivel()
admin.update({'nivel': 'admin', 'descripcion': 'Todopoderoso'})
Mongo(Nivel).add(mortal)

difusion = Comision()
difusion.update({'comision': 'difusion', 'descripcion': 'Promover Morenaje en redes sociales y espacios culturales'})
Mongo(Comision).add(difusion)

arte = Comision()
arte.update({'comision': 'arte', 'descripcion': 'Hacer graficos con estilo'})
Mongo(Comision).add(arte)

log = Comision()
log.update({'comision': 'logistica', 'descripcion': 'Llevar a cabo la planeacion de eventos'})
Mongo(Comision).add(log)

finanzas = Comision()
finanzas.update({'comision': 'finanzas', 'descripcion': 'Manejar las finanzas de el movimiento'})
Mongo(Comision).add(finanzas)

gral = Categoria()
gral.update({'categoria': 'editorial'})
Mongo(Categoria).add(gral)

gral1 = Categoria()
gral1.update({'categoria': 'participa'})
Mongo(Categoria).add(gral1)

gral2 = Categoria()
gral2.update({'categoria': 'contacto'})
Mongo(Categoria).add(gral2)

print "Done.\n"
# Mothafuckin' Done!

