FROM python:3.13

RUN apt-get update && apt-get -y install python3 python3-pip git sqlite3 curl

WORKDIR /shkeeper.io

COPY . .

RUN pip3 install -r requirements.txt

CMD gunicorn \
    --access-logfile - \
    --workers "${GUNICORN_WORKERS:-1}" \
    --threads "${GUNICORN_THREADS:-32}" \
    --worker-class gthread \
    --timeout "${GUNICORN_TIMEOUT:-30}" \
    -b 0.0.0.0:5000 \
    "shkeeper:create_app()"
