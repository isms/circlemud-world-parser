clean:
	find . -name *.pyc -delete
	rm -rf _output/*

test:
	flake8 src/
	python src/tests.py

all: clean
	bash convert_all.sh world/

.PHONY:
	all clean test
