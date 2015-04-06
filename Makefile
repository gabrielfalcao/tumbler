all: install_deps test

PYTHONPATH := $(shell pwd):${PYTHONPATH}
export PYTHONPATH

install_deps:
	@python setup.py develop

test:
	@nosetests -s --verbosity=2 tests --rednose

clean:
	git clean -Xdf

release:
	@./.release
	@python setup.py sdist register upload

run:
	cd examples; python ../tumbler/cli.py run nosql/routes.py
