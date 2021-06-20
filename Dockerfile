FROM python:3.7-slim


RUN apt-get update && \
    apt-get install -y --no-install-recommends build-essential


ADD requirements.txt /
RUN pip install -r /requirements.txt


WORKDIR /srv
ADD src/ /srv
