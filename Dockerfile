FROM python:3.10-bullseye

COPY . /auditlogservice
WORKDIR /auditlogservice

# Environmental variables
ENV MONGO_CLIENT_URL='mongodb://localhost:27017'
ENV MONGO_DB_NAME='auditlogservice'

# Port configuration
EXPOSE 8000

RUN pip install -r requirements.txt
WORKDIR /auditlogservice/api
