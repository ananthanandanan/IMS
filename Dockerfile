FROM python:3.9-slim-buster

# Install dependencies
RUN apt-get update && apt-get install -y \ 
    libpq-dev \
    python3-dev \
    build-essential \
    cron \
    postgresql-client \
    --no-install-recommends && rm -rf /var/lib/apt/lists/*

# Create the log file to be able to run tail
RUN touch /var/log/cron.log

# Test cron job
# RUN crontab -l | { cat; echo "* * * * * echo 'Hello world' >> /var/log/cron.log 2>&1"; } | crontab -

# Create static and media folders
RUN mkdir -p /www/app/staticfiles && \
    mkdir -p /www/app/media

WORKDIR /usr/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY requirements.txt /usr/app/requirements.txt
RUN pip install --upgrade pip \
    && pip install -r /usr/app/requirements.txt

## entry point bash script
COPY ./entrypoint.sh /usr/app/entrypoint.sh
RUN chmod +x /usr/app/entrypoint.sh

## start the entrypoint bash script
ENTRYPOINT ["sh", "/usr/app/entrypoint.sh"]