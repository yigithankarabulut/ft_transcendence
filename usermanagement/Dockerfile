FROM python:3.9

COPY . /app

WORKDIR /app

RUN pip3 install --upgrade pip

RUN pip3 install -r requirements.txt

EXPOSE 8004

CMD ["python3", "manage.py", "runserver", "0.0.0.0:8004"]
