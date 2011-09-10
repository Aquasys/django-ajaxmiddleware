import os

from setuptools import setup, find_packages


MODULE_NAME = 'ajaxmiddleware'

def read( fname ):
    try:
        return open( os.path.join( os.path.dirname( __file__ ), fname ) ).read()
    except IOError:
        return ''


META_DATA = dict(
    name = "ajaxmiddleware",
    version = 1.0,

    author = "Adrien Lemaire",
    author_email = "lemaire.adrien@gmail.com",

    keywords= 'ajax django',
    classifiers=[
        'Intended Audience :: Developers',
        'Programming Language :: Python',
    ],

    packages = find_packages(),
)

if __name__ == "__main__":
    setup( **META_DATA )
