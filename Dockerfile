# Dockerfile
# Date: January 28th 2024
# Author: Justin Meimar
#
# Purpose: Simplify local development and heroku deployment by bundling the build 
#   process into a single, isolated userspace. Deployment becomes configurable with
#   definition of the following environment variables:
#           
#               local (dev)     Heroku
#   PORT:       8000            Auto Assigned 
#   DEBUG:      True            False

FROM ubuntu:latest

EXPOSE 8000
ENV PORT 8000

RUN apt-get update && apt-get install -y curl software-properties-common

# Get Node 20 and Yarn
RUN curl -sL https://deb.nodesource.com/setup_20.x | bash -
RUN apt-get install -y nodejs

# Install Python and pip
RUN apt-get install -y python3 python3-pip

# Set the working directory for Python dependencies
WORKDIR /usr/src/app/backend
COPY backend/requirements.txt .
RUN pip3 install -r requirements.txt

# Set the working directory for Node.js dependencies
WORKDIR /usr/src/app/frontend
COPY frontend/*.json .
RUN npm install

# Copy the source files to the working directory
WORKDIR /usr/src/app
COPY . .

# Set the working directory for running Django commands
WORKDIR /usr/src/app/backend
RUN python3 manage.py collectstatic --noinput

CMD gunicorn deadlybird.wsgi:application --bind 0.0.0.0:$PORT