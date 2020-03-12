FROM python:3.8-alpine

COPY . /app
WORKDIR /app

RUN pip install -r requirements_dev.txt

WORKDIR /app/wykoppl

CMD ["run.sh"]