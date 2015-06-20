test:
	flake8 uu/task/*.py
	./parts/plone/bin/interpreter setup.py test
