"""
Django settings for config project.

Generated by 'django-admin startproject' using Django 3.2.10.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "whitenoise.runserver_nostatic",  # WhiteNoise static files handling
    "django.contrib.staticfiles",
    # REST framework
    "rest_framework",
    "rest_framework.authtoken",
    "dj_rest_auth",
    "corsheaders",
    "django_filters",
    "drf_spectacular",
    "drf_spectacular_sidecar",
    "rest_framework_simplejwt",
    # Local
    "users",
    "repeaters",
    "aprs",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",  # WhiteNoise
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",  # CORS, needs to be here
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            TEMPLATES_DIR,
        ],
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

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = "/static/"
MEDIA_URL = "/media/"

STATIC_ROOT = os.path.join(BASE_DIR, "_deployment/static_root/")
MEDIA_ROOT = os.path.join(BASE_DIR, "_deployment/media_root/")

# WhiteNoise settings

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"


# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# REST framework
REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticatedOrReadOnly",
    ],
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.SessionAuthentication",
        "rest_framework.authentication.TokenAuthentication",
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ],
    "DEFAULT_FILTER_BACKENDS": [
        "django_filters.rest_framework.DjangoFilterBackend",
        "rest_framework.filters.OrderingFilter",
    ],
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.LimitOffsetPagination",
    "PAGE_SIZE": 10,
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    "DEFAULT_PARSER_CLASSES": [
        # Default
        "rest_framework.parsers.JSONParser",
        "rest_framework.parsers.FormParser",
        "rest_framework.parsers.MultiPartParser",
        # 3rd party
        "rest_framework_yaml.parsers.YAMLParser",
    ],
    "DEFAULT_RENDERER_CLASSES": [
        # Default
        "rest_framework.renderers.JSONRenderer",
        "rest_framework.renderers.BrowsableAPIRenderer",
        # 3rd party
        "rest_framework_yaml.renderers.YAMLRenderer",
    ],
}


# Local settings

AUTH_USER_MODEL = "users.User"
X_FRAME_OPTIONS = "SAMEORIGIN"

# Schema
SPECTACULAR_SETTINGS = {
    # Meta
    "TITLE": "Portal do Radioamadorismo: API",
    "VERSION": "1.0.0",
    # Settings
    "SWAGGER_UI_DIST": "SIDECAR",
    "SWAGGER_UI_FAVICON_HREF": "SIDECAR",
    "REDOC_DIST": "SIDECAR",
}

REST_USE_JWT = True
JWT_AUTH_COOKIE = "pr-auth-token"
JWT_AUTH_REFRESH_COOKIE = "pr-refresh-token"


# Settings that should be able to be set by the environment

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ.get("POSTGRES_DB", "radioamadorismo_website_default"),
        "USER": os.environ.get("POSTGRES_USER", "radioamadorismo_website_user"),
        "PASSWORD": os.environ.get(
            "POSTGRES_PASSWORD", "radioamadorismo_website_password"
        ),
        "HOST": os.environ.get("SQL_HOST", "db"),  # Name of the docker service
        "PORT": os.environ.get("SQL_PORT", "5432"),
    }
}

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY", "DO_NOT_USE_THIS_IN_PRODUCTION_")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = int(os.environ.get("DJANGO_DEBUG", default=0))

ALLOWED_HOSTS = os.environ.get(
    "DJANGO_ALLOWED_HOSTS",
    "localhost 127.0.0.1 [::1] backend localhost:8080 localhost:8000",
).split(" ")

CORS_ORIGIN_WHITELIST_DEFAULT = [
    # Default names used by the frontend and backend
    "http://localhost:8080",
    "http://frontend:8080",
    "http://backend:8000",
    "http://localhost:8000",
]
CORS_ORIGIN_WHITELIST = os.environ.get(
    "DJANGO_CORS_ORIGIN_WHITELIST", " ".join(CORS_ORIGIN_WHITELIST_DEFAULT)
).split(" ")

USE_X_FORWARDED_HOST = int(os.environ.get("DJANGO_USE_X_FORWARDED_HOST", False))

EMAIL_BACKEND = os.environ.get(
    "DJANGO_EMAIL_BACKEND", "django.core.mail.backends.console.EmailBackend"
)
EMAIL_HOST = os.environ.get("DJANGO_EMAIL_HOST", "localhost")
EMAIL_PORT = int(os.environ.get("DJANGO_EMAIL_PORT", 25))
EMAIL_HOST_USER = os.environ.get("DJANGO_EMAIL_HOST_USER", "")
EMAIL_HOST_PASSWORD = os.environ.get("DJANGO_EMAIL_HOST_PASSWORD", "")
EMAIL_USE_TLS = int(os.environ.get("DJANGO_EMAIL_USE_TLS", 0))
EMAIL_USE_SSL = int(os.environ.get("DJANGO_EMAIL_USE_SSL", 0))

EMAIL_TIMEOUT = os.environ.get("DJANGO_EMAIL_TIMEOUT", None)
EMAIL_SSL_KEYFILE = os.environ.get("DJANGO_EMAIL_SSL_KEYFILE", None)
EMAIL_SSL_CERTFILE = os.environ.get("DJANGO_EMAIL_SSL_CERTFILE", None)
