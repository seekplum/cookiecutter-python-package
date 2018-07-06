#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

from setuptools import setup, find_packages

root = os.path.dirname(os.path.abspath(__file__))

# 查询版本信息
with open(os.path.join(root, "VERSION")) as f:
    version = f.read().strip()

requirements = []

setup(
    author="{{ cookiecutter.author }}",
    author_email='{{ cookiecutter.email }}',
    classifiers=[
        'Programming Language :: Python :: 2.7',
    ],
    description="{{ cookiecutter.description }}",
    install_requires=requirements,
    include_package_data=True,
    name='{{ cookiecutter.project_slug }}',
    namespace_packages=['{{ cookiecutter.project_slug }}'],
    packages=find_packages(exclude=['tests', 'docs']),
    version=version,
    entry_points={
        'console_scripts': [
        ],
    }
)
