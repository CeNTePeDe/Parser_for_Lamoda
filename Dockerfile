FROM python:3.10

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR /usr/src/Parser_for_Lamoda

COPY Pipfile Pipfile.lock /usr/src/Parser_for_Lamoda/
RUN python -m pip install --upgrade pip
RUN pip install pipenv && pipenv install --system

COPY . .



