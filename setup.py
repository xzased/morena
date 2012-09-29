try:
    from setuptools import setup, find_packages
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup, find_packages

setup(
    name='morena',
    version='1.0',
    description='Pagina Web de Morena',
    author='Ruben Quinones',
    author_email='rq.sysadmin@gmail.com',
    url='http://www.github.com/xzased/morena',
    install_requires=[
        "cherrypy == 3.2.2",
        "jinja2 == 2.6",
        "pymongo == 2.2.1",
        ],
    packages=find_packages(exclude=['ez_setup']),
)