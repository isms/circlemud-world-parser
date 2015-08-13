clean:
	rm *.pyc

test:
	python tests.py

.PHONY:
	clean test