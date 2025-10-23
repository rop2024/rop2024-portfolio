
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent



# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY', 'django-insecure-d6gun472i4%ti(ad$bm)v3$)1@8jil_(k^rglksyn^ji+jz((t')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv('DEBUG', 'True') == 'True'

ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',')


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
    'theme',  # Tailwind CSS app
    'versatileimagefield',

    # Local apps
    'main',
]

# Tailwind configuration
TAILWIND_APP_NAME = 'theme'  # We'll create this later
INTERNAL_IPS = [
    "127.0.0.1",
    "localhost",
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Add this for static files
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
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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


# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'
TIME_ZONE = 'Asia/Kolkata'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
    os.path.join(BASE_DIR, 'theme', 'static'),
]

# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Media files (User uploaded files)
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Static files storage configuration
if DEBUG:
    # Development: use default storage (no compression)
    STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'
else:
    # Production: use WhiteNoise with compression
    STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# VersatileImageField configuration
VERSATILEIMAGEFIELD_SETTINGS = {
    # The amount of time, in seconds, that references to created images
    # should be stored in the cache. Defaults to `2592000` (30 days)
    'cache_length': 2592000,
    
    # The path to the cache key template
    'cache_name': 'versatileimagefield_cache',
    
    # Should be `True` if you want to create progressive JPEGs
    'jpeg_resize_quality': 85,
    
    # A path on disc to an image that will be used as a 'placeholder'
    'placeholder_image_name': None,
    
    # A variable-friendly name for your placeholder image
    'placeholder_image_key': 'placeholder',
    
    # Whether or not to create new images on-the-fly. Set this to `False` for
    # S3 and other backends that don't support on-the-fly image creation
    'create_images_on_demand': True,
    
    # Whether to create progressive JPEGs. Read more about progressive JPEGs
    # here: https://optimus.io/support/progressive-jpeg/
    'progressive_jpeg': True
}

# Production media storage configuration
if not DEBUG:
    # AWS S3 Configuration
    AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
    AWS_STORAGE_BUCKET_NAME = os.getenv('AWS_STORAGE_BUCKET_NAME')
    AWS_S3_REGION_NAME = os.getenv('AWS_S3_REGION_NAME', 'us-east-1')
    AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.{AWS_S3_REGION_NAME}.amazonaws.com'
    AWS_S3_OBJECT_PARAMETERS = {
        'CacheControl': 'max-age=86400',
    }
    
    # Static files configuration
    STATICFILES_STORAGE = 'sitecore.storage_backends.StaticStorage'
    STATIC_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/static/'
    
    # Media files configuration
    DEFAULT_FILE_STORAGE = 'sitecore.storage_backends.PublicMediaStorage'
    MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/media/'
    
    # VersatileImageField configuration for production
    VERSATILEIMAGEFIELD_SETTINGS['create_images_on_demand'] = False
    
    # Alternatively, configure Cloudinary
    # CLOUDINARY_STORAGE = {
    #     'CLOUD_NAME': os.getenv('CLOUDINARY_CLOUD_NAME'),
    #     'API_KEY': os.getenv('CLOUDINARY_API_KEY'),
    #     'API_SECRET': os.getenv('CLOUDINARY_API_SECRET'),
    # }
    # DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'

# Predefined sizes for different use cases
VERSATILEIMAGEFIELD_RENDITION_KEY_SETS = {
    'profile_image': [
        # Square crop for profile pictures
        ('full_size', 'url'),
        ('thumbnail', 'thumbnail__100x100'),
        ('small_square_crop', 'crop__150x150'),
        ('medium_square_crop', 'crop__300x300'),
        ('large_square_crop', 'crop__500x500'),
    ],
    'project_featured': [
        # Various sizes for project featured images
        ('full_size', 'url'),
        ('thumbnail', 'thumbnail__100x75'),
        ('small', 'thumbnail__320x240'),
        ('medium', 'thumbnail__640x480'),
        ('large', 'thumbnail__1024x768'),
        ('hero', 'thumbnail__1600x900'),
        ('square_small', 'crop__150x150'),
        ('square_medium', 'crop__300x300'),
    ],
    'project_gallery': [
        # Sizes for project gallery images
        ('full_size', 'url'),
        ('thumbnail', 'thumbnail__100x75'),
        ('card', 'thumbnail__400x300'),
        ('gallery', 'thumbnail__800x600'),
        ('lightbox', 'thumbnail__1200x900'),
    ],
    'social_share': [
        # Sizes for social media sharing
        ('square', 'crop__400x400'),
        ('facebook', 'crop__1200x630'),
        ('twitter', 'crop__1200x600'),
    ]
}
