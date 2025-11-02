import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Determine environment
ENVIRONMENT = os.getenv('ENVIRONMENT', 'development')

if ENVIRONMENT == 'production':
    from .production import *
else:
    # Development settings
    SECRET_KEY = os.getenv('SECRET_KEY', 'django-insecure-development-key-change-in-production')
    
    DEBUG = os.getenv('DEBUG', 'True').lower() == 'true'
    
    ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', '').split(',') if os.getenv('ALLOWED_HOSTS') else ['localhost', '127.0.0.1']
    
    # Database
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
    
    # Static files (CSS, JavaScript, Images)
    STATIC_URL = '/static/'
    STATIC_ROOT = BASE_DIR / 'staticfiles'
    STATICFILES_DIRS = [
        BASE_DIR / 'static',
        BASE_DIR / 'theme' / 'static',
    ]
    
    # Media files
    MEDIA_URL = '/media/'
    MEDIA_ROOT = BASE_DIR / 'media'
    
    # WhiteNoise configuration
    STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
    
    # Email backend for development
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
    
    # Application definition
    INSTALLED_APPS = [
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        
        # Third-party apps
        'tailwind',
        'theme',
        'versatileimagefield',
        
        # Local apps
        'main',
    ]
    
    MIDDLEWARE = [
        'django.middleware.security.SecurityMiddleware',
        'whitenoise.middleware.WhiteNoiseMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
    ]
    
    ROOT_URLCONF = 'sitecore.urls'
    
    TEMPLATES = [
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': [BASE_DIR / 'templates'],
            'APP_DIRS': True,
            'OPTIONS': {
                'context_processors': [
                    'django.template.context_processors.debug',
                    'django.template.context_processors.request',
                    'django.contrib.auth.context_processors.auth',
                    'django.contrib.messages.context_processors.messages',
                ],
            },
        },
    ]
    
    WSGI_APPLICATION = 'sitecore.wsgi.application'
    
    # Password validation
    AUTH_PASSWORD_VALIDATORS = [
        {
            'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
        },
        {
            'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        },
        {
            'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
        },
        {
            'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
        },
    ]
    
    # Internationalization
    LANGUAGE_CODE = 'en-us'
    TIME_ZONE = 'UTC'
    USE_I18N = True
    USE_TZ = True
    
    # Static files (CSS, JavaScript, Images)
    STATIC_URL = 'static/'
    
    # Default primary key field type
    DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
    
    # Tailwind configuration
    TAILWIND_APP_NAME = 'theme'
    INTERNAL_IPS = ["127.0.0.1"]
    
    # VersatileImageField Configuration
    VERSATILEIMAGEFIELD_SETTINGS = {
        'cache_length': 2592000,
        'cache_name': 'versatileimagefield_cache',
        'jpeg_resize_quality': 85,
        'sized_directory_name': '__sized__',
        'filtered_directory_name': '__filtered__',
        'placeholder_directory_name': '__placeholder__',
        'create_images_on_demand': True,
        'progressive_jpeg': False
    }
    
    VERSATILEIMAGEFIELD_RENDITION_KEY_SETS = {
        'profile_image': [
            ('full_size', 'url'),
            ('thumbnail', 'thumbnail__100x100'),
            ('small_square_crop', 'crop__150x150'),
            ('medium_square_crop', 'crop__300x300'),
            ('large_square_crop', 'crop__500x500'),
        ],
        'project_featured': [
            ('full_size', 'url'),
            ('thumbnail', 'thumbnail__100x75'),
            ('small', 'thumbnail__320x240'),
            ('medium', 'thumbnail__640x480'),
            ('large', 'thumbnail__1024x768'),
            ('hero', 'thumbnail__1600x900'),
        ],
        'project_gallery': [
            ('full_size', 'url'),
            ('thumbnail', 'thumbnail__100x75'),
            ('card', 'thumbnail__400x300'),
            ('gallery', 'thumbnail__800x600'),
            ('lightbox', 'thumbnail__1200x900'),
        ]
    }
