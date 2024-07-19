FROM nginx:alpine

RUN apk update && \
    apk add --no-cache openssl


RUN mkdir -p /etc/ssl/private/ && mkdir -p /etc/ssl/certs/ && \
   openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
   -keyout /etc/ssl/private/nginx.key \
   -out /etc/ssl/certs/nginx.crt \
   -subj "/C=TR/ST=Kocaeli/L=Kocaeli/O=Ecole42/OU=transcendence/CN=127.0.0.1:443"

CMD ["nginx", "-g", "daemon off;"]