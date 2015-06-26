# http://stackoverflow.com/a/30176470/185820
.DEFAULT_GOAL := test

clean:
	python setup.py clean
    
test:
	check-manifest
	pyroma .
	flake8 uu/task/*.py
	./parts/plone/bin/interpreter setup.py test

push:
	git push heroku
