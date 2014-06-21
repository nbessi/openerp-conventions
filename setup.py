# -*- coding: utf-8 -*-
#Taken from pep8-naming flake8 extention
from __future__ import with_statement
from setuptools import setup, find_packages

def get_version(fname='openerp_conventions.py'):
    with open(fname) as f:
        for line in f:
            if line.startswith('__version__'):
                return eval(line.split('=')[-1])

def get_long_description():
    descr = []
    for fname in ('README.rst',):
        with open(fname) as f:
            descr.append(f.read())
    return '\n\n'.join(descr)


setup(
    name='openerp-conventions',
    version=get_version(),
    description="Check OpenERP community conventions, plugin for flake8",
    long_description=get_long_description(),
    install_requires=['flake8'],
    keywords='OpenERP flake8',
    author='Nicolas Bessi',
    author_email='nicolas.bessi@camptocamp.com',
    url='TODO',
    license='Expat license',
    py_modules=['openerp_conventions'],
    packages=find_packages(),
    zip_safe=False,
    entry_points={
        'flake8.extension': [
            '070 = openerp_conventions:OpenERPConventionsChecker',
        ],
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Topic :: Software Development :: Libraries :: OpenERP addons',
        'Topic :: Software Development :: Quality Assurance',
    ],
)
