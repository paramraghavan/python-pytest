"""Minimal setup file for addressbook project."""

from setuptools import setup, find_packages


setup(
    name='aws and pytest',
    version='0.1.0',
    description='aws and pytest',
    packages=find_packages('src'),
    package_dir={'': 'src'},

    # metadata
    author='Param Raghavan',
    author_email='',
    license='mit',
    #install_requires=['pytest']
)
