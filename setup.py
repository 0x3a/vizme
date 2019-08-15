#!/usr/bin/env python3

import os
from setuptools import setup, find_packages

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
        name = 'vizme',
        python_requires='>=3',
        version = '0.1.2',
        author = 'Yonathan Klijnsma',
        author_email = 'admin@0x3a.com',
        url = 'https://github.com/0x3a/vizme',
        packages=find_packages(),
        include_package_data=True,
        description = 'A simple python-based command-line utility to to visualize random blobs of data.',
        long_description=read('README.md'),
        long_description_content_type='text/markdown',
        install_requires=[
            'pypng',
            'ansicolors'
        ],
        entry_points={
            'console_scripts': [
                'vizme=vizme:main',
            ],
        }
     )
