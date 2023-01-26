FROM python:3.9-slim-buster

# Install dependencies

RUN apt-get update && apt-get install -y \ 
    libpq-dev \
    python3-dev \
    build-essential \
    cron \
    postgresql-client \
    --no-install-recommends && rm -rf /var/lib/apt/lists/*

WORKDIR /usr/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY requirements.txt /usr/app/requirements.txt
RUN pip install --upgrade pip \
    && pip install -r /usr/app/requirements.txt