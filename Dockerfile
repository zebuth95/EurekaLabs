FROM python:3.11.1-slim-bullseye

ENV PYTHONDONTWRITEBYTECODE=1

ENV PYTHONUNBUFFERED=1

WORKDIR /usr/src/app

RUN pip install poetry
COPY pyproject.toml poetry.lock ./
RUN poetry config virtualenvs.create false
RUN poetry install --no-interaction --no-root --only main

# copy project
COPY . /usr/src/app/

EXPOSE 8000
