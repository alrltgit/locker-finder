FROM python:3.13-slim

WORKDIR /locker_finder

COPY pyproject.toml .

RUN pip install -e .

COPY . .

RUN apt-get update && apt-get install -y cron

COPY crontab /etc/cron.d/locker-sync
RUN chmod 0644 /etc/cron.d/locker-sync
RUN crontab /etc/cron.d/locker-sync

EXPOSE 5000

CMD ["sh", "-c", "cron && alembic upgrade head && python3 -m src.locker_finder.scripts.seed && flask run --host=0.0.0.0 --port=5000"]