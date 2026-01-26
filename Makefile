clean:
	find . -name *.pyc -delete
	rm -rf _output/*

test:
	uv run pytest src/tests.py -v

lint:
	uv run ruff check src
	uv run ty check

all: clean
	bash convert_all.sh world/

.PHONY:
	all clean test lint
