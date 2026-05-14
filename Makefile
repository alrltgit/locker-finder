.PHONY: install build run up down reset db

install:
	pip install -e .

build:
	docker-compose build --no-cache

up:
	docker-compose up -d

down:
	docker-compose down

reset: down up

seed:
	python3 -m src.locker_finder.scripts.seed

run: build up

setup: install build up seed
