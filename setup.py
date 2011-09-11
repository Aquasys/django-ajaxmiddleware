import os

from setuptools import setup, find_packages


MODULE_NAME = 'ajaxmiddleware'


def read(fname):
    try:
        return open(os.path.join(os.path.dirname(__file__), fname)).read()
    except IOError:
        return ''


META_DATA = dict(
    name="ajaxmiddleware",
    version=0.1,

    author="Adrien Lemaire",
    author_email="lemaire.adrien@gmail.com",
    url='http://github.com/Fandekasp/django-ajaxmiddleware',

    keywords='ajax django',
    classifiers=[
        "Development Status :: 1 - Planning",
        "License :: OSI Approved :: BSD License",
        "Framework :: Django",
        'Intended Audience :: Developers',
        "Operating System :: OS Independent",
        'Programming Language :: Python',
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],

    packages=find_packages(),
)

if __name__ == "__main__":
    setup(**META_DATA)
