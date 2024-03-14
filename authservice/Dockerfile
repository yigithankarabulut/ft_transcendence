FROM alpine:3.7

RUN apk add --no-cache python3-dev \
    && pip3 install --upgrade pip

COPY . /app

WORKDIR /app

RUN pip3 install -r requirements.txt

EXPOSE 8001

CMD [ "python3", "manage.py", "runserver", "0.0.0.0:8001"]
