from setuptools import setup, find_packages
import os

here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(here, 'README.md'), encoding='utf-8') as fh:
    long_description = fh.read()

with open('requirements.txt') as f:
    install_requires = f.read().splitlines()

VERSION = '0.0.1'
DESCRIPTION = 'Retrieve given location features using OpenStreetMap'
LONG_DESCRIPTION = 'Library that utilizes the OpenStreetMap (OSM) database and Overpass API to retrieve location features and perform various calculations based on the given location.'

# Setting up
setup(
    name='osmlf',
    version=VERSION,
    author='ccan23',
    author_email='dev.ccanb@protonmail.com',
    url='https://github.com/ccan23/osmlf',
    license='MIT',
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=find_packages(),
    install_requires=install_requires,
    keywords=['python', 'map', 'openstreetmap', 'amenities', 'location', 'coordinates', 'latitude', 'longitude'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: MIT License'
    ]
)