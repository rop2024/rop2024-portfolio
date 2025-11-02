#!/bin/bash

echo "Starting deployment process..."

# Check if we're in production mode
if [ "$ENVIRONMENT" = "production" ]; then
    echo "Production environment detected"
    
    # Run migrations
    echo "Running database migrations..."
    python manage.py migrate
    
    # Collect static files
    echo "Collecting static files..."
    python manage.py collectstatic --noinput
    
    # Build Tailwind CSS for production
    echo "Building Tailwind CSS..."
    cd theme/static_src
    npm run production
    cd ../..
    
    # Create superuser if needed (first deploy)
    if [ "$CREATE_SUPERUSER" = "true" ]; then
        echo "Creating superuser..."
        python manage.py createsuperuser --noinput || true
    fi
    
    # Optimize images if needed
    echo "Optimizing images..."
    python manage.py optimize_images || true
    
else
    echo "Development environment detected"
    
    # Run migrations
    python manage.py migrate
    
    # Collect static files
    python manage.py collectstatic --noinput
    
    # Build Tailwind CSS for development
    cd theme/static_src
    npm run build
    cd ../..
fi

echo "Deployment preparation complete!"