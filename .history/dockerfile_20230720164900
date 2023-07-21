FROM python:3.8

ENV PYTHONUNBUFFERED 1

WORKDIR /code

ARG DB_NAME
ARG DB_USER
ARG DB_PASSWORD

RUN apt-get update

COPY requirements.txt /code/

RUN pip install -r requirements.txt

COPY . /code/