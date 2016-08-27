#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import setup, find_packages


with open('README.rst') as f:
    readme = f.read()

with open('requirements.txt') as f:
    requires = f.readlines()

setup(
    name='python-memcached-rate-limit',
    version='0.0.1',
    description=u'',
    long_description=readme,
    author=u'Krishna Pennacchioni',
    author_email=u'krishna@agentelinux.com.br',
    url=u'https://github.com/agentelinux/python-memcached-rate-limit',
    license=u'MIT',
    packages=find_packages(exclude=('tests', 'docs')),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'License :: OSI Approved :: MIT License'
    ],
    install_requires=requires
)