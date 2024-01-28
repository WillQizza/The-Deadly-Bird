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

FROM node:20

# Install python and pip
RUN apt-get update && apt-get install -y python3 python3-pip

# Install python dependencies
WORKDIR /usr/src/app/backend
COPY backend/requirements.txt .
RUN pip3 install -r requirements.txt

# Install node dependencies
WORKDIR /usr/src/app/frontend
COPY frontend/*.json .
RUN yarn install 

# Copy source files
WORKDIR /usr/src/app
COPY . .

# Collect static files
WORKDIR /usr/src/app/backend
RUN python3 manage.py collectstatic --noinput

CMD ["gunicorn", "deadlybird.wsgi:application", "--bind", "0.0.0.0:$PORT"]