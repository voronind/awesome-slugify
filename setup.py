# coding=utf8

from setuptools import setup
import os

version = '1.0.1'

name = 'awesome-slugify'
package = 'slugify'
description = 'Python flexible slugify module'
url = 'https://github.com/dimka665/awesome-slugify'
author = 'Dmitry Voronin'
author_email = 'dimka665@gmail.com'
license = 'BDSM'
install_requires = [
    'Unidecode==0.04.14',
    ]
classifiers = [
    'Intended Audience :: Developers',
    'License :: OSI Approved :: BSD License',
    'Operating System :: POSIX',
    'Programming Language :: Python',
]


def get_packages(package):
    return [dirpath for dirpath, dirnames, filenames in os.walk(package)
            if os.path.exists(os.path.join(dirpath, '__init__.py'))]


setup(
    name=name,
    version=version,
    url=url,
    license=license,
    description=description,
    author=author,
    author_email=author_email,
    packages=get_packages(package),
    py_modules=['slugify/slugify'],
    install_requires=install_requires,
    classifiers=classifiers,
    keywords='slugify,alternative russian slugify, flexible, awesome',
)


