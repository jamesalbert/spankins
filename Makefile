clean:
	rm -rf build dist spankins.egg-info

package: clean
	python setup.py sdist bdist_wheel
	twine upload --repository-url https://upload.pypi.org/legacy/ dist/*
