FROM python:3.11-slim

WORKDIR /app

PYTHONBUFFER 1

PYTHONENV 1

COPY .requirements.txt .

RUN pip install -r requirements.txt --no-cache

COPY . .

