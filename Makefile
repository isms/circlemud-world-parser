clean:
	rm -f *.pyc
	rm -rf output/*

test:
	flake8
	python tests.py

.PHONY:
	clean test