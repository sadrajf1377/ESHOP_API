FROM python:3.11-slim

WORKDIR /app

ENV PYTHONWRITEBYTECODE 1


COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

