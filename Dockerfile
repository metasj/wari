FROM python:3.8-slim

LABEL maintainer="Dennis Priskorn <priskorn@riseup.net>"

ENV DOCKER=true

COPY pyproject.toml .

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir poetry && \
    poetry install

#EXPOSE 8000