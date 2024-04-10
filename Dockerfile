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

# Install Node.js dependencies
RUN corepack enable pnpm
WORKDIR /app/frontend
COPY frontend/*.json .
RUN pnpm install

# Receive args from compose file, default to port 8000 for prod.
ARG LIVE_HOST_URL "http://localhost:8000"
ARG REACT_APP_BASE_URL "http://localhost:8000"

ENV REACT_APP_BASE_URL ${REACT_APP_BASE_URL}
ENV PUBLIC_URL ${LIVE_HOST_URL}

# Compile frontend
COPY ./frontend/ /app/frontend/
RUN mkdir -p /app/backend/react/static
RUN mkdir -p /app/backend/react/templates
RUN pnpm run build

FROM python:3 AS backend
ENV PORT 8000

ARG LIVE_HOST_URL "http://localhost:8000"
ARG AUTH_USERNAME "username"
ARG AUTH_PASSWORD "password"
ARG GITHUB_API_TOKEN ""
ARG STRIPE_API_KEY "sk_test_51OIZXzLmClgbbAeLhE6c2Ji2YmVtNSSGWq91H8xBDl7BKGwKz5QaeutsBEXWtL495ysuRBXDHypPiBQvzGyPo5Hb00RIPGJiOU"
ARG STRIPE_WEBHOOK_SECRET ""
ARG STRIPE_MONTHLY_PRICE_ID "price_1P2fzcLmClgbbAeLjS9LdyXx"
ARG STRIPE_YEARLY_PRICE_ID "price_1P2oY2LmClgbbAeL92dGotVx"
ENV DOCKER 1

ENV HOST_URL ${LIVE_HOST_URL}
ENV REMOTE_AUTH_USERNAME ${AUTH_USERNAME}
ENV REMOTE_AUTH_PASSWORD ${AUTH_PASSWORD}
ENV GITHUB_API_TOKEN ${GITHUB_API_TOKEN}
ENV STRIPE_API_KEY ${STRIPE_API_KEY}
ENV STRIPE_WEBHOOK_SECRET ${STRIPE_WEBHOOK_SECRET}
ENV STRIPE_MONTHLY_PRICE_ID ${STRIPE_MONTHLY_PRICE_ID}
ENV STRIPE_YEARLY_PRICE_ID ${STRIPE_YEARLY_PRICE_ID}

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
ENV PYTHONUNBUFFERED TRUE
CMD python3 manage.py migrate && gunicorn deadlybird.wsgi:application --bind 0.0.0.0:$PORT --threads 4 --access-logfile '-' --error-logfile '-'