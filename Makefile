clean:
	rm -f *.pyc
	rm -rf output/*

test:
	flake8
	python tests.py

all: clean
	bash convert_all.sh world/

.PHONY:
	all clean test