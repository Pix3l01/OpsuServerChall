FROM python:3.9
RUN apt-get update
COPY ./app /app
COPY ./requirements.txt /app

RUN pip install -r /app/requirements.txt
ENTRYPOINT ["python", "-u", "/app/app.py"]