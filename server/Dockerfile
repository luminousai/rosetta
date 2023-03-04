FROM python:3.11

RUN pip install poetry

WORKDIR /app

COPY data data
COPY src src
COPY pyproject.toml .
COPY poetry.lock .

RUN poetry install

EXPOSE 8081
