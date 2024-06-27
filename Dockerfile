# We chose Python 3.11 full variant as other variants lacks some tools necessary
# to build this project's dependencies
FROM python:3.13

# Establish /code as working directory in the container
WORKDIR /code

# Copy production requirements and install dependencies
COPY ./requirements-production.txt requirements.txt
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy source code into the working directory
COPY ./app ./app
COPY finesse-weights.json .

# Use Gunicorn as the server, configuring it for the Flask app
ENTRYPOINT gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 --forwarded-allow-ips "*" app:app
