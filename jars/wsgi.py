"""
WSGI config for jar project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/howto/deployment/wsgi/
"""

import os, sys
sys.path.append('/etc/jars')
try:
    from jars_config import env_settings
    for key, value in env_settings:
        os.environ[key] = value
except ImportError:
    pass
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "jars.mysql_settings")
os.environ.setdefault("REDIS_URL", "redis://")

from django.core.wsgi import get_wsgi_application

application = get_wsgi_application()
