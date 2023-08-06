from setuptools import setup

setup(
    name='ProxyMan',
    version='0.0.1',
    description='A simple proxy manager for Python with WebShare API support',
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