clean:
	find . -name *.pyc -delete
	rm -rf _output/*

test:
	uv run pytest -v

lint:
	uv run isort --check-only circlemud_world_parser
	uv run ruff check circlemud_world_parser
	uv run ty check

all: clean
	bash convert_all.sh assets/

.PHONY:
	all clean test lint
