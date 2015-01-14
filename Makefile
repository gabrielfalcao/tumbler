all: install_deps test

export PYTHONPATH := ${PWD}:${PYTHONPATH}


install_deps:
	@python setup.py develop

test:
	@nosetests -s --verbosity=2 tests --rednose

clean:
	git clean -Xdf

release:
	@./.release
	@python setup.py sdist register upload
