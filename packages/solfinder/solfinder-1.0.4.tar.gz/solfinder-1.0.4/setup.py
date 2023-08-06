from setuptools import setup
from codecs import open
from os import path

with open(path.join(path.abspath(path.dirname(__file__)), 'README.md'), encoding='utf8') as f:
    long_description = f.read()

setup(
    name='solfinder',
    version='1.0.4',
    packages=['solfinder'],
    url='',
    license='GNU LGPLv3',
    author='fcastino',
    author_email='f.castino@tudelft.nl',
    description='SolFinder 1.0.4',
    long_description_content_type="text/markdown",
    long_description=long_description,
    include_package_data=True,
)
