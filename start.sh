#!/bin/bash

# Production startup script for Render deployment

echo "Starting Stock AI Backend..."

# Set default values for production
export APP_HOST=${APP_HOST:-"0.0.0.0"}
export APP_PORT=${APP_PORT:-"8000"}
export DEBUG=${DEBUG:-"false"}

# Check if we're in production mode
if [ "$DEBUG" = "false" ]; then
    echo "Running in production mode with gunicorn..."
    exec gunicorn api.main:app \
        --bind $APP_HOST:$APP_PORT \
        --workers 2 \
        --worker-class uvicorn.workers.UvicornWorker \
        --timeout 120 \
        --keep-alive 5 \
        --max-requests 1000 \
        --max-requests-jitter 100 \
        --access-logfile - \
        --error-logfile - \
        --log-level info
else
    echo "Running in development mode with uvicorn..."
    exec python run.py
fi 