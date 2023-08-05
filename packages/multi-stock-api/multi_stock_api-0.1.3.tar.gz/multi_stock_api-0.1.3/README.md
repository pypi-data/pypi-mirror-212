# multi-stock-api
Library for accessing data from multiple stock markets without an official API

Updating pypi library:
1. Change setup.py version value
2. Execute:
python setup.py sdist bdist_wheel
twine check dist/*
twine upload dist/*
