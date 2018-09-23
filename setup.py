#!/usr/bin/env python
from setuptools import setup

setup(
    name='git-taxbreak',
    description='git taxbreak tool',
    author='Kamil Luczak',
    author_email='kamil.luczak@luczakweb.pl',
    keywords='git taxbreak',
    url='https://github.com/kluczak/git-taxbreak',
    version='0.1',
    py_modules=['git_taxbreak'],
    install_requires=[
        'gitpython',
    ],
    entry_points={
        'console_scripts': [
            'git-taxbreak = git_taxbreak:main'
        ]
    }
)
