from setuptools import setup, find_packages

import codecs
import chardet

def get_encoding(file):
    with open(file, 'rb') as f:
        return chardet.detect(f.read())['encoding']

encoding = get_encoding('requirements.txt')
install_requires = codecs.open('requirements.txt', 'r', encoding=encoding).read().splitlines()
 
setup(
    name='myPackageLicensePrototype',
    version='1.0.8',
    description='Description of your package',
    install_requires=install_requires,
    packages=find_packages(),
)


# from setuptools import setup, find_packages

#from myPackageLicensePrototype import __version__

# Read requirements from requirements.txt
# import codecs
# import chardet
# def get_encoding(file):
#     with open(file, 'rb') as f:
#         return chardet.detect(f.read())['encoding']

# encoding = get_encoding('requirements.txt')
# install_requires = codecs.open('requirements.txt', 'r', encoding=encoding).read().splitlines()

# Package information
# setup(
#     name='myPackageLicensePrototype ',
#     version='1.0.0',

#     url='https://github.com/da-roth/PackageLicensePrototype',
#     author='Daniel Roth',
#     author_email='daniel-roth@posteo.org',

#     install_requires=install_requires,
#     packages=find_packages(),
#     include_package_data=True,
#     package_data={'': ['src/*.py']}
# )