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

run: build up

setup: install build up

create:
	mkdir -p postgres_data
	cp -n .env.example .env

setup: create install build up
