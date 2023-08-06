# PackageLicensePrototype

# Activate virtual environment
.venv\Scripts\activate.bat  


# Package publish to pypi.org

python setup.py sdist

cd dist

pip install twine

twine upload myPackageLicensePrototype-1.0.x.tar.gz


# Compiled publish

pip install --upgrade setuptools wheel
python setup.py bdist_wheel
twine upload dist/* 

# Pyarmer (make sure not to use venv or at least don't show in requirements, it's not needed for use)

pip install pyarmor
pyarmor gen PackageContent.py


