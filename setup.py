from setuptools import setup, find_packages
from codecs import open
from os import path

import os
import re
from setuptools import Command

here = path.abspath(path.dirname(__file__))
with open(path.join(here, 'requirements.txt'), encoding='utf-8') as f:
    all_reqs = f.read().split('\n')

install_requires = [x.strip() for x in all_reqs if 'git+' not in x]
dependency_links = [x.strip().replace('git+', '') for x in all_reqs if x.startswith('git+')]

setup(
    # Application name:
    name="Barriers",

    # Version number (initial):
    version="0.1.0",

    # Application author details:
    author="name surname",
    author_email="name@addr.ess",

    # Packages
    packages=find_packages(exclude=['docs', 'tests*']),

    # Include additional files into the package
    include_package_data=True,

    # Details
    url="http://pypi.python.org/pypi/MyApplication_v010/",

    #
    # license="LICENSE.txt",
    description="Useful towel-related stuff.",

    # long_description=open("README.txt").read(),

    # Dependent packages (distributions)
    install_requires=install_requires,
    dependency_links=dependency_links,
    entry_points={
        'console_scripts': [
            'barrier = src.barrier:main'
        ]},
)