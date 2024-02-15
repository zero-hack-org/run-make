ARG PYTHON_IMAGE_TAG=3.11.8

FROM python:$PYTHON_IMAGE_TAG AS builder

ENV PYTHONUNBUFFERED 1

WORKDIR /app

RUN pip install "poetry==1.7.1"

COPY pyproject.toml poetry.lock /app/


FROM builder AS runner

RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi

EXPOSE 8000