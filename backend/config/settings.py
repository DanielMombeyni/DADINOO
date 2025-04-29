"""
Django settings for config project.
"""

import os
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent


SECRET_KEY = "django-insecure-8(2s*#a8wm9^f$+@9)zidada*a(fgqlg8vr*_on##f-qmf$%gc"

DEBUG = True

ALLOWED_HOSTS = ["*"]

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.sites",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "daphne",
    "django.contrib.staticfiles",
    "rest_framework",
    "drf_spectacular",
    "django_filters",
    "rest_framework.authtoken",
    "corsheaders",
    "core",
    "api",
    "chat",
    "channels",
]

# Auth
INSTALLED_APPS += [
    # "allauth",
    # "allauth.account",
    # "allauth.socialaccount",
    # "allauth.socialaccount.providers.google",
    # "social_django",
]

AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "rest_framework.authentication.TokenAuthentication",
    # "allauth.account.auth_backends.AuthenticationBackend",
    # "social_core.backends.google.GoogleOAuth2",
]

SITE_ID = 1

LOGIN_REDIRECT_URL = "/"
ACCOUNT_LOGOUT_REDIRECT_URL = "/"

SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = "YOUR_GOOGLE_CLIENT_ID"
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = "YOUR_GOOGLE_CLIENT_SECRET"

SOCIALACCOUNT_PROVIDERS = {
    "google": {
        "APP": {
            "client_id": "your-google-client-id",
            "secret": "your-google-client-secret",
            "key": "",
        }
    }
}

ACCOUNT_AUTHENTICATION_METHOD = "email"
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = False

# Middleware

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    # "allauth.account.middleware.AccountMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"
ASGI_APPLICATION = "config.asgi.application"


# Database

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "HOST": os.environ.get("DB_HOST"),
        "NAME": os.environ.get("DB_NAME"),
        "USER": os.environ.get("DB_USER"),
        "PASSWORD": os.environ.get("DB_PASS"),
    }
}

# Allowed Host front proxy

CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",  # React dev server
    "http://localhost:4200",  # Angular dev server
    "http://localhost:19000",  # react native dev server
    "http://192.168.1.13:19000",  # react native dev server
]

CSRF_TRUSTED_ORIGINS = ["http://localhost", "http://192.168.1.13"]

CORS_ALLOW_ALL_ORIGINS = True


AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


STATIC_URL = "/static/static/"
# MEDIA_URL = "/static/media/"
MEDIA_URL = "/media/"

MEDIA_ROOT = "/vol/web/media"
STATIC_ROOT = "/vol/web/static"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


AUTH_USER_MODEL = "core.User"

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.TokenAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    "TEST_REQUEST_DEFAULT_FORMAT": "json",
}

SPECTACULAR_SETTINGS = {
    "COMPONENT_SPLIT_REQUEST": True,
}

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.example.com"
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = "your_email@example.com"
EMAIL_HOST_PASSWORD = "your_email_password"
DEFAULT_FROM_EMAIL = "noreply@example.com"


DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
