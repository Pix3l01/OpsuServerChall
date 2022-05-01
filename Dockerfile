FROM python:3.9
RUN apt-get update
COPY ./app /app
COPY ./requirements.txt /app

WORKDIR /app

RUN pip install -r ./requirements.txt
ENTRYPOINT ["./gunicorn.sh"]