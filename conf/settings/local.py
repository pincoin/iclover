from .base import *

DEBUG = True

# SECURITY WARNING: Keep them secret!
SECRET_KEY = Secret.SECRET_KEY
ALLOWED_HOSTS = Secret.ALLOWED_HOSTS
DATABASES = Secret.DATABASES

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/assets/'
STATIC_ROOT = os.path.join(BASE_DIR, 'assets/')
STATICFILES_DIRS = [
]

# Media files (Uploaded files)
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')

# Our own apps
INSTALLED_APPS += [
    'core',
    'member',
    'shop',
]
