FROM python:3.10-slim-buster

WORKDIR /app

ARG PORT=5001

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

ENV UVICORN_PORT=$PORT

CMD [ "uvicorn", "--host", "0.0.0.0", "api.main:app" ]
