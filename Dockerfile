FROM python:3.10

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR /usr/src/parser_for_lamoda

COPY Pipfile Pipfile.lock /usr/src/parser_for_lamoda/
RUN python -m pip install --upgrade pip
RUN pip install pipenv && pipenv install --system

COPY . .

