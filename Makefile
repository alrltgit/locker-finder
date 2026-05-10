.PHONY: install build run

dev:
	pip install -e ".[dev]"

install:
	pip install -e .

build:
	python3 -m build

run:
	python3 -m locker_finder.main