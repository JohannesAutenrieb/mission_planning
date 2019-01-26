# -*- coding: utf-8 -*-


from setuptools import setup, find_packages


with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='TaskAllocationSystem',
    version='0.1.0',
    description='Task Allocation System for a UAV Swarm',
    long_description=readme,
    author='Team A Cranfiel University',
    author_email='',
    url='',
    license=license,
    packages=find_packages(exclude=('tests', 'docs'))
)

