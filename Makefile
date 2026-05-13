include .env
export

.PHONY: install build run up down reset db

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

db:
	docker exec -it ${POSTGRES_DB} psql -U ${POSTGRES_USER} -d ${POSTGRES_DB}

setup: build up seed
