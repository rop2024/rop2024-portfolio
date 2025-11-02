import os
from .settings import *

# Load environment variables
load_dotenv()

# Try to import dj-database-url (for paid tier with PostgreSQL)
try:
    import dj_database_url
    HAS_DJ_DATABASE_URL = True
except ImportError:
    HAS_DJ_DATABASE_URL = False

# Security settings
DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'
SECRET_KEY = os.getenv('SECRET_KEY')

# Allowed hosts
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', '').split(',')

# SSL/HTTPS settings
SECURE_SSL_REDIRECT = not DEBUG
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SESSION_COOKIE_SECURE = not DEBUG
CSRF_COOKIE_SECURE = not DEBUG

# Database - fallback to SQLite for free tier
DATABASE_URL = os.getenv('DATABASE_URL')
if DATABASE_URL and HAS_DJ_DATABASE_URL:
    DATABASES = {
        'default': dj_database_url.config(
            default=DATABASE_URL,
            conn_max_age=600,
            conn_health_checks=True,
        )
    }
else:
    # Free tier: use SQLite (data will reset on redeploy)
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

# Static files (WhiteNoise)
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Media files configuration - simplified for free tier
# Use local storage (files will be lost on redeploy)
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Note: For free tier, external storage (S3/Cloudinary) is not configured
# Files uploaded to the portfolio will be lost when the service spins down

# Email configuration - disabled for free tier
# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'  # Logs to console

# Security headers - simplified for free tier
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = 'DENY'

# Logging - simplified for free tier
# Uses default Django logging (to console)

# VersatileImageField for production
VERSATILEIMAGEFIELD_SETTINGS['create_images_on_demand'] = False