from setuptools import setup, find_packages
import codecs
import os


VERSION = '0.0.2'
DESCRIPTION = 'Projekt zal - pip'
LONG_DESCRIPTION = 'Loooooong descreption'

# Setting up
setup(
    name="PD_pip_Kajetan",
    version=VERSION,
    author="Kajetan Fornalik",
    description=DESCRIPTION,
    packages=find_packages(),
    install_requires=['numpy', 'pandas'],
    keywords=['python', 'ProjektZal']
)



