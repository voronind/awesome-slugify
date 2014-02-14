# coding=utf8

from setuptools import setup
import os

version = '1.2'

name = 'awesome-slugify'
package = 'slugify'
description = 'Python flexible slugify module'
url = 'https://github.com/dimka665/awesome-slugify'
author = 'Dmitry Voronin'
author_email = 'dimka665@gmail.com'
license = 'GNU GPLv3'
install_requires = [
    'Unidecode',
    ]
classifiers = [
    'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
    'Programming Language :: Python',
    'Programming Language :: Python :: 2',
    'Programming Language :: Python :: 2.6',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.3',
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


