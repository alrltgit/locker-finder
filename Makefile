.PHONY: install build run

install:
	pip install -e .

build:
	python3 -m build

run:
	python3 -m locker_finder.main