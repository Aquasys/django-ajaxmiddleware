#!/usr/bin/env python
from setuptools import setup, find_packages
import sys


MODULE_NAME = 'ajaxmiddleware'

REQUIRES = ['Django>=1.3', ]
if sys.version_info < (2, 7):
    REQUIRES.append("ordereddict>=1.1")


META_DATA = dict(
    name="django-ajaxmiddleware",
    version="0.2.2",
    description="django middleware to handle ajax requests really easily",
    author="Adrien Lemaire",
    author_email="lemaire.adrien@gmail.com",
    url='https://github.com/Aquasys/django-ajaxmiddleware/',

    keywords='django ajax json',
    classifiers=[
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: BSD License",
        "Framework :: Django",
        'Intended Audience :: Developers',
        "Operating System :: OS Independent",
        'Programming Language :: Python',
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    install_requires=REQUIRES,
    packages=find_packages(exclude=["testapp", ]),
    include_package_data=True,
    zip_safe=False,
)

if __name__ == "__main__":
    setup(**META_DATA)
