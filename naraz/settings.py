from pathlib import Path
import os
from datetime import timedelta
from decouple import config,Csv

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='', cast=Csv())


# Application definition ------------------------------------------------------

INSTALLED_APPS = [
    # Django core apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    "django.contrib.sites",
    # Third-party apps
    'django_cleanup.apps.CleanupConfig',
    "corsheaders",  # Handles Cross-Origin Resource Sharing (CORS) headers
    'rest_framework',  # Django REST Framework core
    'drf_spectacular',
    'rest_framework_simplejwt',  # JWT authentication for DRF
    'rest_framework_simplejwt.token_blacklist',
    # Local apps
    'account.apps.AccountConfig',  # Custom application for user accounts/authentication
    'products',
    'shop',
    'cart',
]

SITE_ID = 1


# Django REST Framework Settings ------------------------------------------------------
# Configures authentication and permission settings for the Django REST Framework
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    # Global pagination settings
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    # "PAGE_SIZE": 10,
}

FRONTEND_URL = config("FRONTEND_URL")
REACT_RESET_URL = config("PASSWORD_RESET_URL")


# SPECTACULAR configuration (Required)
SPECTACULAR_SETTINGS = {
    'TITLE': 'Your Project API Documentation',
    'DESCRIPTION': 'Documentation for all endpoints of the project.',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
}


SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=5),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
}


# Middleware Configuration
# ----------------------------------------------------------------------
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    # Handles Cross-Origin Resource Sharing (CORS) headers
    "corsheaders.middleware.CorsMiddleware",
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# Custom User Model
# ----------------------------------------------------------------------
AUTH_USER_MODEL = 'account.User'

ROOT_URLCONF = 'naraz.urls'


# Template Configuration
# ----------------------------------------------------------------------
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]


# WSGI Configuration
# ----------------------------------------------------------------------
WSGI_APPLICATION = 'naraz.wsgi.application'
# ASGI_APPLICATION = 'naraz.asgi.application'


# Database
# https://docs.djangoproject.com/en/6.0/ref/settings/#databases
# ----------------------------------------------------------------------

DATABASES = {
    'default': {
        'ENGINE': config("DB_ENGINE", default="django.db.backends.sqlite3"),
        'NAME': BASE_DIR / config("DB_NAME", default="db.sqlite3"),
    }
}

# Email Configuration
# ----------------------------------------------------------------------
# -----------------Email Settings-----------------
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = config("EMAIL_HOST")
EMAIL_PORT = config("EMAIL_PORT", cast=int)
EMAIL_USE_TLS = config("EMAIL_USE_TLS", cast=bool)
EMAIL_HOST_USER = config("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = config("EMAIL_HOST_PASSWORD")
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER


# Password validation
# https://docs.djangoproject.com/en/6.0/ref/settings/#auth-password-validators
# ----------------------------------------------------------------------

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
# https://docs.djangoproject.com/en/6.0/topics/i18n/
# ----------------------------------------------------------------------

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Dhaka'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/6.0/howto/static-files/
# ----------------------------------------------------------------------

STATIC_URL = config('STATIC_URL', default='/static/')
STATIC_ROOT = config('STATIC_ROOT', default='staticfiles')
STATICFILES_DIRS = [os.path.join(BASE_DIR, config('STATICFILES_DIRS', default='static'))]

MEDIA_URL = config('MEDIA_URL', default='/media/')
MEDIA_ROOT = os.path.join(BASE_DIR, config('MEDIA_ROOT', default='media'))

# CORS Settings
# ----------------------------------------------------------------------
CORS_ALLOWED_ORIGINS = config('CORS_ALLOWED_ORIGINS', cast=Csv())
CSRF_TRUSTED_ORIGINS = config('CSRF_TRUSTED_ORIGINS', default='', cast=Csv())
CSRF_COOKIE_SECURE = config('CSRF_COOKIE_SECURE', default=False, cast=bool)
SESSION_COOKIE_SECURE = config('SESSION_COOKIE_SECURE', default=False, cast=bool)
CORS_ALLOW_CREDENTIALS = config('CORS_ALLOW_CREDENTIALS', default=True, cast=bool)


# Celery Configuration
CELERY_BROKER_URL = config('CELERY_BROKER_URL')
CELERY_RESULT_BACKEND = config('CELERY_RESULT_BACKEND')

CELERY_TASK_ALWAYS_EAGER = config('CELERY_TASK_ALWAYS_EAGER', default=False, cast=bool)
CELERY_TASK_EAGER_PROPAGATES = config('CELERY_TASK_EAGER_PROPAGATES', default=False, cast=bool)

CELERY_ACCEPT_CONTENT = config('CELERY_ACCEPT_CONTENT', default='json', cast=Csv())
CELERY_TASK_SERIALIZER = config('CELERY_TASK_SERIALIZER', default='json')
CELERY_RESULT_SERIALIZER = config('CELERY_RESULT_SERIALIZER', default='json')