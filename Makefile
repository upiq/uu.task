# http://stackoverflow.com/a/30176470/185820
.DEFAULT_GOAL := build

build:
	buildout -v

clean:
	python setup.py clean
    
check-manifest:
	check-manifest
	pyroma .

check-lint:
	flake8 setup.py
	flake8 uu/task/

check-test:
	bin/test -s uu.task -v

check: check-manifest check-lint check-test

test: check
	viewdoc

coverage:
	bin/coverage
	bin/report

push:
	git push heroku
