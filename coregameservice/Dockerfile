FROM python:3.9-slim-buster

WORKDIR /app

COPY . .

RUN apt-get update && apt-get install -y --no-install-recommends \
    python3-pip \
 && pip3 install --no-cache-dir -r requirements.txt \
 && apt-get purge -y --auto-remove python3-pip \
 && rm -rf /var/lib/apt/lists/* \
 && rm -rf requirements.txt

EXPOSE 8000

CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]
