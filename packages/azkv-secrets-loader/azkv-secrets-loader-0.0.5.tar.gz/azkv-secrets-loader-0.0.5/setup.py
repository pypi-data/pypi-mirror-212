from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

VERSION = '0.0.5'
DESCRIPTION = 'A package for loading Azure Key Vault Secrets.'
LONG_DESCRIPTION = 'A package for loading Azure Key Vault Secrets.'

# Setting up
setup(
    name="azkv-secrets-loader",
    version=VERSION,
    author="Richard",
    author_email="<rich_swainson@hotmail.co.uk>",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[
        'azure-identity' ,
        'azure-keyvault-secrets',
        'azure-core'
    ],
    keywords=['azure', 'api', 'keyvault'],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)