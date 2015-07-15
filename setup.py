from setuptools import find_packages, setup

setup(
    name='mri',
    packages=find_packages(exclude=['scripts', 'tests']),
    version='0.05')
