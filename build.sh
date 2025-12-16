#!/usr/bin/env bash
# Build script for Render deployment

set -o errexit  # Exit on error

# Navigate to backend directory
cd backend

# Install Python dependencies
echo "Installing Python dependencies..."
pip install -r requirements.txt

# Install additional Render-specific requirements
echo "Installing Render-specific dependencies..."
if [ -f "../requirements-render.txt" ]; then
    pip install -r ../requirements-render.txt
fi

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Run database migrations
echo "Running database migrations..."
python manage.py migrate

echo "Build completed successfully!"
