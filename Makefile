clean:
	find . -name *.pyc -delete
	rm -rf _output/*

test:
	flake8 src/
	python src/tests.py

all: clean
	bash convert_all.sh world/

lint:
	black --check .
	flake8 .

.PHONY:
	all clean test
