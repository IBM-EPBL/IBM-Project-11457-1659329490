# syntax=docker/dockerfile:1

FROM python:3.9.15-slim-buster

WORKDIR /expense-tracker

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

RUN python3 -m flask init-db
CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]