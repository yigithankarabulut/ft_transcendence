FROM alpine:3.7

RUN apk add --no-cache python3 python3-dev py3-pip build-base libffi-dev openssl-dev

COPY . /app

WORKDIR /app

RUN pip3 install --upgrade pip \
    && pip3 install -r requirements.txt

EXPOSE 8001

CMD ["python3", "manage.py", "runserver", "0.0.0.0:8001"]
