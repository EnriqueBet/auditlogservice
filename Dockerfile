FROM python:3.10-bullseye

# Required files
ADD api /auditlogservice/api
ADD app.py /auditlogservice/app.py
ADD requirements.txt /auditlogservice/requirements.txt

# Install requirements and change to workdir
RUN pip install -r /auditlogservice/requirements.txt
WORKDIR /auditlogservice

# Port configuration
EXPOSE 8000

# Environmental variables (this variables are set for a local build)
ENV SERVICE_BASE_URL=0.0.0.0
ENV SERVICE_PORT=80

# Set entry point
ENTRYPOINT uvicorn app:app --host=$SERVICE_BASE_URL --port=$SERVICE_PORT
