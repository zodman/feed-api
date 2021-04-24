FROM python:3.9-slim

RUN python -m pip install --upgrade pip
ENV PYTHONUNBUFFERED=1
RUN mkdir -p /app
WORKDIR /app
COPY requirements.txt /app/requirements.txt
RUN python -m pip install -r /app/requirements.txt
COPY . /app
