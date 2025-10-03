#!/bin/bash
# Startup script for Railway deployment

# Get the port from environment variable, default to 8000 if not set
PORT=${PORT:-8000}

echo "Starting Vision AI Box Counting API on port $PORT..."

# Start the FastAPI application
exec uvicorn main:app --host 0.0.0.0 --port $PORT
