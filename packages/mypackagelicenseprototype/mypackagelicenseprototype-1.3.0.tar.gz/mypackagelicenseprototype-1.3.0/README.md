# PackageLicensePrototype



# Package publish to pypi.org

python setup.py sdist

cd dist

pip install twine

twine upload myPackageLicensePrototype-1.0.x.tar.gz
