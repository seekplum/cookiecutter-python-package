#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

version = '0.1.0'

setup(
    author="{{ cookiecutter.author }}",
    author_email='{{ cookiecutter.email }}',
    classifiers=[
        'Programming Language :: Python :: 2.7',
    ],
    description="{{ cookiecutter.description }}",
    install_requires=[

    ],
    scripts=[

    ],
    setup_requires=[

    ],
    include_package_data=True,
    name='{{ cookiecutter.project_name }}',
    namespace_packages=['{{ cookiecutter.project_slug }}'],
    packages=find_packages(exclude=['tests', 'docs']),
    version=version,
    entry_points={
        'console_scripts': [
        ],
    }
)
