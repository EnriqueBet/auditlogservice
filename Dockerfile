FROM python:3.10-bullseye

COPY . api/

WORKDIR api/

RUN pip install -r requirements.txt
