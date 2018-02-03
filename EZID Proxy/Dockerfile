FROM python:3

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .
COPY wsgi.py .
EXPOSE 80

RUN uwsgi --socket 0.0.0.0:8000 --protocol=http -w wsgi
