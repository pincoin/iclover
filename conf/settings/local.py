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

REST_FRAMEWORK_TOKEN = 'e8b0ddbbe7152d35771a20c6669d1c2016175580'

# Our own apps
INSTALLED_APPS += [
    'core',
    'member',
    'design',
    'managing',
    'api',
]
