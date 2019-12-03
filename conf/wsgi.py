import os
from conf.settings.secret import Secret

from django.core.wsgi import get_wsgi_application

module_name = 'conf.settings'
if not Secret:
    module_name = module_name+'.local'

os.environ.setdefault('DJANGO_SETTINGS_MODULE', module_name)

application = get_wsgi_application()
