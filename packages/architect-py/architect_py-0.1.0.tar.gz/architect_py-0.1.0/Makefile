.PHONY: clean build upload-test upload

clean:
	rm -rf dist

build:
	python3 -m build

upload-test:
	python3 -m twine upload --repository testpypi dist/*

upload:
	python3 -m twine upload --repository pypi dist/*

# Testing package from test PyPI
#
# pip install -i https://test.pypi.org/simple/ \
#   --extra-index-url https://pypi.org/simple \
#   architect-py