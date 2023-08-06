from setuptools import setup, find_packages

setup(
    name='callapi',
    version='1.0.0',
    packages=find_packages(),
    install_requires=['requests'],
    url='https://github.com/abhashbhai17/callapi',
    author='Abhash',
    author_email='abhashsaha2008@gmail.com',
    description='A Python module for making API calls to the CallAPI service.',
)
