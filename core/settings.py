"""
Django settings for core project.

Generated by 'django-admin startproject' using Django 4.0.5.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""
import os
import sys
from pathlib import Path

import stringcase
from asbool import asbool
from loguru import logger
from stela import settings

from core import __version__
from core.services.sentry import configure_sentry
from core.tools.debug import show_toolbar

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
PROJECT_NAME = stringcase.titlecase(settings["project.name"])


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/
ENV = settings["ENV"]
RUNNING_TESTS = "pytest" in sys.modules or "test" in sys.argv
SERVICE_TYPE = settings["project.service_type"]
SHOW_DJANGO_PAGES = settings["project.show_django_pages"]

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = settings["project.secret_key"]

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = asbool(settings["project.debug"])

ALLOWED_HOSTS = settings["project.allowed_hosts"]

LOGIN_URL = "/admin/login"

TOOLBAR_ALLOWED_HOSTS = [
    "localhost:8080",
    "localhost:8081",
    "127:0.0.1:8081",
]

DEBUG_TOOLBAR_CONFIG = {"SHOW_TOOLBAR_CALLBACK": show_toolbar, "SHOW_COLLAPSED": True}

REST_FRAMEWORK = {
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    "DEFAULT_RENDERER_CLASSES": [
        "core.tools.serializers.JSONCamelRenderer",
    ],
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.SessionAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework_api_key.permissions.HasAPIKey",
    ],
    "DEFAULT_THROTTLE_RATES": {"anon": "6/minute"},
    "DEFAULT_PARSER_CLASSES": [
        "core.tools.serializers.JSONCamelParser",
        "core.tools.serializers.FormCamelParser",
        "core.tools.serializers.MultiPartCamelParser",
    ],
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 25,
}

if DEBUG:
    REST_FRAMEWORK["DEFAULT_RENDERER_CLASSES"].append(
        "core.tools.serializers.BrowsableAPICamelRenderer",
    )

SWAGGER_DESCRIPTION = """
### Welcome to Bhub Customer API Challenge
#### Environment is: {env}

Please check the following links to understand *OpenAPI* specifications:
* [OpenAPI Specification](https://swagger.io/specification/)
* [DRF Spectacular](https://github.com/tfranzel/drf-spectacular)
"""


SPECTACULAR_SETTINGS = {
    "TITLE": "Bhub Customer API",
    "DESCRIPTION": SWAGGER_DESCRIPTION.format(env=ENV.upper()),
    "VERSION": __version__,
}

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "corsheaders",
    "debug_toolbar",
    "django_filters",
    "drf_spectacular",
    "rest_framework",
    "rest_framework_api_key",
    "customers.apps.CustomersConfig",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

if DEBUG and asbool(settings["project.show_debug_toolbar"]):
    logger.warning("Debug toolbar is enabled")
    MIDDLEWARE.insert(0, "debug_toolbar.middleware.DebugToolbarMiddleware")

ROOT_URLCONF = "core.urls"

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

WSGI_APPLICATION = "core.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

if RUNNING_TESTS:
    logger.debug("Starting Internal Database for Unit Tests...")
else:
    logger.info(f"Configuring Database {settings['db.name']}...")

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": "postgres" if RUNNING_TESTS else settings["db.name"],
        "USER": "postgres" if RUNNING_TESTS else settings["db.user"],
        "PASSWORD": "postgres" if RUNNING_TESTS else settings["db.password"],
        "HOST": "db" if RUNNING_TESTS else settings["db.host"],
        "PORT": "5432" if RUNNING_TESTS else settings["db.port"],
    },
}


# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation."
        "UserAttributeSimilarityValidator",
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
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = "pt-br"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = "static/"
STATIC_ROOT = os.path.join(BASE_DIR, "static")

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Google Apps Authentication
EMAIL_ALLOWABLE_DOMAIN = "megalus.com.br"

# CORS
CORS_ALLOW_ALL_ORIGINS = asbool(settings["project.allow_all_origins"])
CORS_ALLOW_HEADERS = ("content-type", "authorization", "accept", "origin", "user-agent")

# Cache
CACHES = {
    "default": {
        "BACKEND": f"django.core.cache.backends.{settings['cache.backend']}",
        "LOCATION": f'{settings["cache.host"]}:{settings["cache.port"]}',
        "KEY_PREFIX": f"customer-api-{ENV}-",
    },
}
if "dummy" in settings["cache.backend"]:
    logger.warning("Memory Cache is Disabled.")

PROVIDER_EXTRA_DATA_CACHE_TIMEOUT = 60 * 60 * 24


if not RUNNING_TESTS:
    configure_sentry()
