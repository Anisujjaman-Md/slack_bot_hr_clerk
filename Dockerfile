FROM python:3.8.2-alpine3.11
ENV PYTHONUNBUFFERED 1
RUN apk update && \
    apk add --virtual build-deps gcc python-dev musl-dev jpeg-dev zlib-dev && \
    apk add postgresql-dev libxml2-dev libxslt-dev freetype-dev libffi-dev
ENV LIBRARY_PATH=/lib:/usr/lib
RUN mkdir /code
WORKDIR /code
COPY requirements.txt /code/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
COPY . /code/
