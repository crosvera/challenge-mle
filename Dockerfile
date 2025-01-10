# syntax=docker/dockerfile:1.2
FROM python:3.10-bookworm
# put you docker configuration here

RUN pip install -U pip && pip install pipenv

WORKDIR /app

COPY ./data ./data
COPY ./challenge ./challenge
COPY Pipfile .
COPY Pipfile.lock .

RUN pipenv install -v

CMD ["pipenv", "run", "uvicorn", "challenge.api:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]