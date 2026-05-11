include .env
export

.PHONY: up down reset db

up:
	docker-compose up -d

down:
	docker-compose down

reset: down up

seed:
	python3 -m src.locker_finder.scripts.seed

db:
	docker exec -it ${POSTGRES_DB} psql -U ${POSTGRES_USER} -d ${POSTGRES_DB}