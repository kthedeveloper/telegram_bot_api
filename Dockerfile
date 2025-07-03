FROM python:3.12

WORKDIR /app

EXPOSE 8080

COPY ./requirements.txt /app

RUN pip install -r requirements.txt --no-cache-dir

COPY ./src /app

ENTRYPOINT ["python", "run.py"]