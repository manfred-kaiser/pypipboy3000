from distutils.core import setup
from setuptools import find_packages

setup(
    name='pypipboy',
    version='0.0.1',
    description='Python PIP Boy',
    author='Manfred Kaiser',
    author_email='manfred.kaiser@logfile.at',
    url='https://github.com/manfred-kaiser/pypipboy3000',
    packages=find_packages(),
    package_data={
        'pypipboy': [
            'data/*.*',
            'data/images/*.*',
            'data/images/map_icons/*.*',
            'data/sounds/*.*'
        ],
    },
    entry_points={
        'console_scripts': ['pypipboy=pypipboy.main:main'],
    },
    install_requires=[
        'pygame',
        'requests',
        'xmltodict',
        'numpy'
    ]
)
