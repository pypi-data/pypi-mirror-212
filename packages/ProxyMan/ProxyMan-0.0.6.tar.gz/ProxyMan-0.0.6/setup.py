import os

from setuptools import setup

import ProxyMan

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

# Get version from init file
setup(
    name='ProxyMan',
    version=ProxyMan.__version__,
    description='A simple proxy manager for Python with WebShare API support',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/rawandahmad698/ProxyMan',
    author='Rawand Ahmed Shaswar',
    author_email='rawa@rawa.dev',
    license='BSD 3-Clause License',
    packages=['ProxyMan'],
    install_requires=['aiohttp'],
    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3.7',
    ],
)