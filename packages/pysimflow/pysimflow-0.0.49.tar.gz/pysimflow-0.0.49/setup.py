#!/usr/bin/env python
# coding: utf-8

from setuptools import setup

setup(
    name='pysimflow',
    version='0.0.49',
    author='sl.truman',
    author_email='sl.truman@live.com',
    url='',
    description=u'',
    packages=['digitaltwin','digitaltwin_data'],
    install_requires=[
        'numpy',
        'pybullet',
        'scipy'
    ],
    include_package_data=True
)
