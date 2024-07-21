FROM python:3-slim

COPY . /app

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev

RUN pip3 install --upgrade pip

RUN pip3 install -r requirements.txt

COPY start.sh /app/start.sh

RUN chmod +x /app/start.sh

EXPOSE 8010

ENTRYPOINT ["sh", "./start.sh"]

# CMD ["gunicorn", "--capture-output", "--bind", "0.0.0.0:8010", "gameservice.wsgi", "--workers=3"]

CMD ["python3", "manage.py", "runserver", "0.0.0.0:8010"]