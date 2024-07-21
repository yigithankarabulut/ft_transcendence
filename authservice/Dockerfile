FROM python:3-slim

COPY . /app

WORKDIR /app

RUN pip3 install --upgrade pip

RUN pip3 install -r requirements.txt

EXPOSE 8001

CMD [ "python3", "manage.py", "runserver", "0.0.0.0:8001"]
