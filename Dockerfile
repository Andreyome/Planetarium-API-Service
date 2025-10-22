FROM python:3.11.6-alpine3.18
LABEL maintainer="andreyomem@gmail.com"

WORKDIR /planetarium

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .


