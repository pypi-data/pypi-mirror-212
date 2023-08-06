#!/usr/bin/env python

import sys
import os
from os.path import dirname
from setuptools import find_packages, setup

BASE_DIR = os.path.dirname(os.path.realpath(__file__))

if os.path.exists(BASE_DIR) and os.path.isdir(BASE_DIR):
    sys.path.insert(0, BASE_DIR)
else:
    raise ValueError('Error in Path')


def get_file_contents(filename):
    with open(os.path.join(dirname(__file__), filename)) as fp:
        return fp.read()


def get_install_requires():
    requirements = get_file_contents('requirements.txt')
    install_requires = []
    for line in requirements.split('\n'):
        line = line.strip()
        if line and not line.startswith('-'):
            install_requires.append(line)
    return install_requires


setup(
    name='auth-token-django',
    description='Django token authentication',
    version = "0.0.2",
    author='Shivin Agarwal',
    long_description=get_file_contents('README.md'),
    author_email='shivin.agarwal15@gmail.com',
    url='https://github.com/Shivin01/django_auth_token',
    classifiers=[
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Programming Language :: Python :: 3.9'
    ],
    install_requires=get_install_requires(),
    include_package_data=True,
    keywords='django auth token',
    packages=find_packages(exclude=['tests*']),
    package_data={
        # If any package contains *.so or *.pyi or *.lic files or *.key files,
        # include them:
        "": ["*.so", "*.pyi", "*.lic", "*.key", "*.html"],
    },
)