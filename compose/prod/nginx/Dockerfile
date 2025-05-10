FROM docker.io/nginx:1.28.0-alpine@sha256:aed99734248e851764f1f2146835ecad42b5f994081fa6631cc5d79240891ec9
COPY ./compose/prod/nginx/default.conf /etc/nginx/conf.d/default.conf
COPY ./certs/ /etc/nginx/certs