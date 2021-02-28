# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='inaturalist-remote-manager',
    version='0.1.0',
    description='Basic iNaturalist client',
    long_description=readme,
    author='Valentin Hamon',
    author_email='hamonvalentin7@gmail.com',
    url='https://github.com/vhamon/inaturalist-remote-manager',
    license=license,
    packages=find_packages(exclude=('tests', 'docs'))
)