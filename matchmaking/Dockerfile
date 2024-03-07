FROM python:3.9

COPY . /app

WORKDIR /app

RUN pip3 install --upgrade pip

RUN pip3 install -r requirements.txt

CMD ["python3", "manage.py", "runserver", "8007"]