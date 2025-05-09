FROM docker.io/nginx:1.17.8-alpine@sha256:9e81b8f9cef5a095f892183688798a5b2c368663276aa0f2be4b1cd283ace53d
COPY ./compose/prod/nginx/default.conf /etc/nginx/conf.d/default.conf
COPY ./certs/ /etc/nginx/certs