from setuptools import setup, find_packages

setup(
    name='mypackagelicenseprototype',
    version='1.3.0',
    description='Description of your package',
    packages=find_packages(where="src"),  # Required
    # Specify which Python versions you support. In contrast to the
    # 'Programming Language' classifiers above, 'pip install' will check this
    # and refuse to install the project if the version does not match. See
    # https://packaging.python.org/guides/distributing-packages-using-setuptools/#python-requires
    python_requires=">=3.7, <4",
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