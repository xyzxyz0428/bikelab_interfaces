from setuptools import find_packages
from setuptools import setup

setup(
    name='bikelab_interfaces',
    version='0.0.0',
    packages=find_packages(
        include=('bikelab_interfaces', 'bikelab_interfaces.*')),
)
