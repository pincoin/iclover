from .base import *

DEBUG = True

# SECURITY WARNING: Keep them secret!
SECRET_KEY = Secret.SECRET_KEY
ALLOWED_HOSTS = Secret.ALLOWED_HOSTS
DATABASES = Secret.DATABASES


if DEBUG:
    # Static files (CSS, JavaScript, Images)
    STATIC_URL = '/assets/'
    STATIC_ROOT = os.path.join(BASE_DIR, 'assets/')
    STATICFILES_DIRS = [
    ]
    # Media files (Uploaded files)
    MEDIA_URL = '/media/'
    MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')
else:
    # AWS Setting
    AWS_REGION = Secret.AWS_REGION
    AWS_STORAGE_BUCKET_NAME = Secret.AWS_STORAGE_BUCKET_NAME
    AWS_ACCESS_KEY_ID = Secret.AWS_ACCESS_KEY_ID
    AWS_SECRET_ACCESS_KEY = Secret.AWS_SECRET_ACCESS_KEY
    AWS_QUERYSTRING_AUTH = False
    AWS_S3_HOST = f's3.{AWS_REGION}.amazonaws.com'
    AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'
    AWS_DEFAULT_ACL = None
    # Static Setting
    STATIC_URL = '/assets/'
    # Media Setting
    MEDIA_URL = '/media/'

    DEFAULT_FILE_STORAGE = 'conf.settings.storage.MediaStorage'
    STATICFILES_STORAGE = 'conf.settings.storage.StaticStorage'

    MEDIAFILES_LOCATION = 'media'
    STATICFILES_LOCATION = 'assets'

REST_FRAMEWORK_TOKEN = 'e8b0ddbbe7152d35771a20c6669d1c2016175580'

# Our own apps
INSTALLED_APPS += [
    'core',
    'member',
    'design',
    'managing',
    'api',
    'imagekit',
    'mathfilters',
    'storages',
]


# logging
LOGGING = {
    'version': 1,
    # 기존의 로깅 설정을 비활성화 할 것인가?
    'disable_existing_loggers': False,

    # 포맷터
    # 로그 레코드는 최종적으로 텍스트로 표현됨
    # 이 텍스트의 포맷 형식 정의
    # 여러 포맷 정의 가능
    'formatters': {
        'format1': {
            'format': '[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s',
            'datefmt': '%d/%b/%Y %H:%M:%S'
        },
        'format2': {
            'format': '%(levelname)s %(message)s'
        },
    },

    # 핸들러
    # 로그 레코드로 무슨 작업을 할 것인지 정의
    # 여러 핸들러 정의 가능
    'handlers': {
        # 콘솔(터미널)에 출력
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'format2',
        }
    },

    # 로거
    # 로그 레코드 저장소
    # 로거를 이름별로 정의
    'loggers': {
        'django.db.backends': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
    },

}