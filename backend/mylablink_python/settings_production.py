import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env.production")

from .settings import *  # استيراد الإعدادات الأساسية من settings.py

# ---- إعدادات الإنتاج ----
DEBUG = os.getenv('DEBUG', 'False') == 'True'
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY')

# ALLOWED_HOSTS - دعم متقدم
allowed_hosts_env = os.getenv('ALLOWED_HOSTS', '')
if allowed_hosts_env:
    ALLOWED_HOSTS = [host.strip() for host in allowed_hosts_env.split(',') if host.strip()]
else:
    # القيم الافتراضية للإنتاج
    ALLOWED_HOSTS = ['.onrender.com', '127.0.0.1', 'localhost']

# ---- إعدادات الأمان ----
SECURE_SSL_REDIRECT = os.getenv('SECURE_SSL_REDIRECT', 'True') == 'True'
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 31536000  # سنة واحدة
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# ---- إعداد قاعدة البيانات ----
# دعم DATABASE_URL من Render (PostgreSQL) أو MySQL التقليدي
if os.getenv('DATABASE_URL'):
    # استخدام DATABASE_URL للقواعد البيانات على Render
    try:
        import dj_database_url
        DATABASES = {
            'default': dj_database_url.config(
                default=os.getenv('DATABASE_URL'),
                conn_max_age=600,
                conn_health_checks=True,
            )
        }
    except ImportError:
        print("WARNING: dj-database-url not installed. Falling back to manual configuration.")
        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.mysql',
                'NAME': os.getenv('MYSQL_DB'),
                'USER': os.getenv('MYSQL_USER'),
                'PASSWORD': os.getenv('MYSQL_PASSWORD'),
                'HOST': os.getenv('MYSQL_HOST', '127.0.0.1'),
                'PORT': os.getenv('MYSQL_PORT', '3306'),
                'CONN_MAX_AGE': int(os.getenv('CONN_MAX_AGE', 600)),
            }
        }
else:
    # MySQL التقليدي
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': os.getenv('MYSQL_DB'),
            'USER': os.getenv('MYSQL_USER'),
            'PASSWORD': os.getenv('MYSQL_PASSWORD'),
            'HOST': os.getenv('MYSQL_HOST', '127.0.0.1'),
            'PORT': os.getenv('MYSQL_PORT', '3306'),
            'OPTIONS': {
                'charset': 'utf8mb4',
                'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
            },
            'CONN_MAX_AGE': int(os.getenv('CONN_MAX_AGE', 600)),
        }
    }

# ---- إعداد البريد ----
EMAIL_BACKEND = os.getenv('EMAIL_BACKEND')
EMAIL_HOST = os.getenv('EMAIL_HOST')
EMAIL_PORT = int(os.getenv('EMAIL_PORT', 587))
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
EMAIL_USE_TLS = os.getenv('EMAIL_USE_TLS', 'True') == 'True'
DEFAULT_FROM_EMAIL = os.getenv('DEFAULT_FROM_EMAIL')

# ---- static & media ----
STATIC_ROOT = BASE_DIR / "staticfiles"
MEDIA_ROOT = BASE_DIR / "mediafiles"

# ---- Logging للإنتاج - متوافق مع Render ----
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': os.getenv('DJANGO_LOG_LEVEL', 'INFO'),
            'propagate': False,
        },
        'django.request': {
            'handlers': ['console'],
            'level': 'ERROR',
            'propagate': False,
        },
    },
}

# ---- CORS للإنتاج ----
CORS_ALLOW_ALL_ORIGINS = os.getenv('CORS_ALLOW_ALL', 'False') == 'True'

# ---- رسائل التحقق ----
print("=" * 60)
print("🚀 PRODUCTION SETTINGS LOADED SUCCESSFULLY")
print(f"   DEBUG: {DEBUG}")
print(f"   ALLOWED_HOSTS: {ALLOWED_HOSTS}")
print(f"   DATABASE ENGINE: {DATABASES['default']['ENGINE']}")
print(f"   STATIC_ROOT: {STATIC_ROOT}")
print("=" * 60)

