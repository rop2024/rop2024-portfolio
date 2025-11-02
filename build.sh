#!/usr/bin/env bash
# Exit on error
set -o errexit

# Install dependencies
pip install -r requirements.txt

# Build Tailwind CSS
cd theme/static_src
npm install
npm run production
cd ../..

# Collect static files
python manage.py collectstatic --noinput

# Run migrations
python manage.py migrate