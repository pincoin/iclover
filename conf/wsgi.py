import os
from conf.settings.secret import Secret

from django.core.wsgi import get_wsgi_application

module = None
if not Secret:
    module = '.local'

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'conf.settings'+module)

application = get_wsgi_application()
