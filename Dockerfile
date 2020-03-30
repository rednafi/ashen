
FROM python:3.8.2-slim-buster

RUN mkdir app/

WORKDIR /app

COPY requirements.txt /app

ENV FLASK_DEBUG 1
ENV FLASK_APP flask_run.py

RUN pip install -r requirements.txt

EXPOSE 4000

COPY . /app

CMD ["gunicorn", "-b", "0.0.0.0:5000", "flask_run:application"]
