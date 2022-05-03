FROM python:3.9
RUN apt-get update
COPY ./app /app
COPY ./requirements.txt /app

WORKDIR /app

RUN pip install -r ./requirements.txt
RUN chmod +x ./gunicorn.sh
ENTRYPOINT ["./gunicorn.sh"]
#ENTRYPOINT ["python", "-m", "flask", "run", "--host=0.0.0.0"]
