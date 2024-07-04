FROM python:3.11-slim as base

RUN apt-get update

WORKDIR /
RUN mkdir /logs
RUN mkdir -p /static/audio
RUN mkdir -p /data

# Copy the requirements.txt file to the container
COPY ./requirements.txt /

# Install dependencies using pip
RUN pip3 install --no-cache-dir -r /requirements.txt

# Pre-download Flair model
RUN python -c "from flair.models import SequenceTagger; SequenceTagger.load('ner')"

### DEVELOPMENT ###
FROM base as development

# Copy your application code into the container
COPY . .

CMD ["uvicorn", "app.api:app", "--host", "0.0.0.0", "--port", "8001", "--reload", "--reload-dir", "/app", "--access-log"]

### PRODUCTION ###
FROM base as production

# Copy your application code into the container
COPY . .

# Install production dependencies using pip
RUN pip3 install --no-cache-dir -r /requirements.txt

CMD ["gunicorn", "-k", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8001", "app.api:app"]
