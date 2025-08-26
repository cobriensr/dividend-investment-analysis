#!/bin/bash
# Start database in background
docker-compose up db -d

# Wait for DB to be ready
echo "Waiting for database..."
sleep 3

# Start backend and frontend locally
concurrently \
  "cd backend && uvicorn app.main:app --reload" \
  "cd frontend && npm run dev:all"