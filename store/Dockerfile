FROM python:3

MAINTAINER James Byars

WORKDIR /app
ADD . /app
RUN pip install -r requirements.txt


ENTRYPOINT sleep 15; python store.py