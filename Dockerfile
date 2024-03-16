# Dockerfile
# Date: Feburary 16 2024
# Author: Justin Meimar & William Qi
#
# Purpose: Simplify local development and heroku deployment by bundling the build 
#   process into a single, isolated userspace. Deployment becomes configurable with
#   definition of the following environment variables:
#           
#               local (dev)     Heroku
#   PORT:       8000            Auto Assigned 
#   DEBUG:      True            False

# Get Node 20 and pnpm
FROM node:20 AS frontend
ENV REACT_APP_BASE_URL ""

# Install Node.js dependencies
RUN corepack enable pnpm
WORKDIR /app/frontend
COPY frontend/*.json .
RUN pnpm install

# Compile frontend
COPY ./frontend/ /app/frontend/
RUN mkdir -p /app/backend/react/static
RUN mkdir -p /app/backend/react/templates
RUN pnpm run build

FROM python:3 AS backend
ENV PORT 8000

ARG LIVE_HOST_URL "http://localhost:8000/"
ARG AUTH_USERNAME "username"
ARG AUTH_PASSWORD "password"
ENV DOCKER 1

ENV HOST_URL ${LIVE_HOST_URL}
ENV REMOTE_AUTH_USERNAME ${AUTH_USERNAME}
ENV REMOTE_AUTH_PASSWORD ${AUTH_PASSWORD}

# Install Python dependencies
WORKDIR /app
COPY backend/requirements.txt .
RUN pip3 install -r requirements.txt

# Copy backend source + frontend build files to backend deployment
COPY ./backend .
COPY --from=frontend /app/backend/react/static/ /app/react/static/
COPY --from=frontend /app/backend/react/templates/ /app/react/templates/

# Compile static files and run app
RUN python3 manage.py collectstatic --noinput
CMD python3 manage.py migrate && gunicorn deadlybird.wsgi:application --bind 0.0.0.0:$PORT