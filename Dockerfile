# pull official base image
FROM python:3.9-alpine

# set work directory
WORKDIR /app

# Sets whether the app is run on a remote system
ARG REMOTE=0 
ARG APP_NAME
ARG SECRET_KEY

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

ENV DEBUG=0

ENV DJANGO_APP_NAME=$APP_NAME
ENV DJANGO_SECRET_KEY=$SECRET_KEY

# install psycopg2
RUN apk update \
    && apk add --virtual build-deps gcc python3-dev musl-dev \
    && apk add postgresql-dev \
    && pip install psycopg2 \
    && apk del build-deps

# install dependencies
COPY ./boilerplate/requirements.txt .
RUN pip install -r requirements.txt

# copy project
COPY . .

# add and run as non-root user
RUN adduser -D myuser
USER myuser

# run gunicorn
CMD cd ./boilerplate && python manage.py collectstatic && gunicorn boilerplate.wsgi:application --bind 0.0.0.0:$PORT