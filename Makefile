include .env
export

.PHONY: install build run up down reset db

up:
	docker-compose up -d

down:
	docker-compose down

reset: down up

seed:
	python3 -m src.locker_finder.scripts.seed

setup: up seed

db:
	docker exec -it ${POSTGRES_DB} psql -U ${POSTGRES_USER} -d ${POSTGRES_DB}

build:
	docker-compose build --no-cache
