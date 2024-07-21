FROM python:3-slim

COPY . /app

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev

RUN pip3 install --upgrade pip

RUN pip3 install -r requirements.txt

EXPOSE 8011

CMD ["daphne", "gameplayservice.asgi:application", "-b", "0.0.0.0", "-p", "8011"]
