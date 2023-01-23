FROM ubuntu:latest

RUN apt-get update && apt-get install -y cron && apt-get install pip -y

# Create the log file to be able to run tail
RUN touch /var/log/cron.log
# Setup cron job
# RUN (crontab -l ; echo "* * * * * echo "Hello world" >> /var/log/cron.log") | crontab
RUN crontab -l | { cat; echo "* * * * * echo 'Hello world' >> /var/log/cron.log 2>&1"; } | crontab -

# CMD /usr/sbin/cron && tail -f /var/log/cron.log

WORKDIR /usr/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY requirements.txt /usr/app/requirements.txt
RUN pip install -r requirements.txt

CMD service cron start && python3 manage.py runserver 0.0.0.0:8000