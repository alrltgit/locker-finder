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

init:
	mkdir -p postgres_data
	cp -n .env.example .env

setup: install build up
