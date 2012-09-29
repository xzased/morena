INSTALACION
===========
Para instalar morena solo tienes que ejecutar el bootstrap script bajo el directorio utils::

    ./utils/bootstrap.sh

Esto instalara solo el paquete base, para inicializar la base de datos pasa la opcion init-db::

    ./utils/bootstrap.sh init-db

.. note::
    Debes estar bajo un ambiente virtual.


DEV SERVER
==========
Para correr el servidor de prueba usa el comando runserver bajo el directorio utils::

    ./utils/runserver.py

By default it will run on port 8080.


SERVIDOR DE PRODUCCION
======================
La aplicacion esta diseniada para ser montada como wsgi app usando apache como el servidor
principal, modifica los parametros necesarios en el archivo bajo utils/apache (principalmente
la inicializacion de el ambiente virtual) y listo.