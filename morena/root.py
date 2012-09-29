from org import *
from public import *
from galerias import *
from usuarios import *
from articulos import *


root = Public()
org = Org()
org.articulos = Articulos()
org.galerias = Galerias()
root.org = org