"""
WSGI config for MyLabLink project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/stable/howto/deployment/wsgi/
"""

import os
from django.core.wsgi import get_wsgi_application

# استخدام DJANGO_SETTINGS_MODULE من متغيرات البيئة
# في بيئة الإنتاج (Render)، سيتم تعيينها إلى 'mylablink_python.settings_production'
# في بيئة التطوير المحلية، ستستخدم 'mylablink_python.settings'
os.environ.setdefault(
    'DJANGO_SETTINGS_MODULE',
    os.getenv('DJANGO_SETTINGS_MODULE', 'mylablink_python.settings')
)

application = get_wsgi_application()
