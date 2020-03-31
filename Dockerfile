FROM python:3.8-alpine

COPY . /app
WORKDIR /app

RUN \
    apk add --no-cache build-base libpq gcc && \
    apk add --no-cache python3-dev musl-dev libffi-dev postgresql postgresql-dev && \
    apk add --no-cache libxml2-dev libxslt-dev libxml2

RUN pip install -r requirements_dev.txt

WORKDIR /app/zeug

CMD ["/app/zeug/run.sh"]
