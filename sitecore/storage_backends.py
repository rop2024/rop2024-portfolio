from django.conf import settings

try:
    from storages.backends.s3boto3 import S3Boto3Storage
    HAS_S3 = True
except ImportError:
    HAS_S3 = False
    S3Boto3Storage = None

class StaticStorage(S3Boto3Storage):
    location = 'static'
    default_acl = 'public-read'

class PublicMediaStorage(S3Boto3Storage):
    location = 'media'
    default_acl = 'public-read'
    file_overwrite = False

class PrivateMediaStorage(S3Boto3Storage):
    location = 'private'
    default_acl = 'private'
    file_overwrite = False
    custom_domain = False

# Cloudinary configuration (alternative to S3)
def configure_cloudinary():
    try:
        import cloudinary
        import cloudinary.uploader
        import cloudinary.api
        
        cloudinary.config(
            cloud_name=settings.CLOUDINARY_CLOUD_NAME,
            api_key=settings.CLOUDINARY_API_KEY,
            api_secret=settings.CLOUDINARY_API_SECRET,
            secure=True
        )
    except ImportError:
        raise ImportError("Cloudinary package is not installed. Install it with: pip install cloudinary")