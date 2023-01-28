"""
Django settings for ims project.

Generated by 'django-admin startproject' using Django 3.1.13.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""
import os
from pathlib import Path
import logging

from collections import OrderedDict
import environ


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

env = environ.Env()
environ.Env.read_env()

SECRET_KEY = env.str(
    "SECRET_KEY", default="czif=j6p5yagrslg#(1axv35%#-+_x02fff=kzg06r3lc*8i*9"
)

DEBUG = env.bool("DEBUG", default=True)

ALLOWED_HOSTS = [
    "*"
]  # in production, this should be the domain name of the server or the IP address of the server
AUTH_USER_MODEL = "members.Members"
CORS_ALLOW_ALL_ORIGINS = True  # in production, this should be False

# Application definition

INSTALLED_APPS = [
    "corsheaders",
    "rest_framework",
    "mathfilters",
    "buildings",
    "admin_interface",
    "members",
    "colorfield",
    "admin_reorder",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "huey.contrib.djhuey",  # <--- huey task queue for background tasks
    "easy_select2",
    "django_filters",
    "crispy_forms",
    "userlog",
]
APP_ORDER = [
    ("Buildings"),
    ("Blocks"),
    ("Floors"),
    ("Rooms"),
    ("Departments"),
    ("Items"),
]

X_FRAME_OPTIONS = "SAMEORIGIN"
SILENCED_SYSTEM_CHECKS = ["security.W019"]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "admin_reorder.middleware.ModelAdminReorder",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "ims.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates")],
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

WSGI_APPLICATION = "ims.wsgi.application"
ASGI_APPLICATION = "ims.asgi.application"

# Database

## Postgres Database

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": env.str("DJANGO_NAME", default=""),
        "USER": env.str("DJANGO_USER", default=""),
        "PASSWORD": env.str("DJANGO_PASSWORD", default=""),
        "HOST": "db",
        "PORT": "5432",
    }
}


ADMIN_REORDER = (
    {"app": "admin_interface", "label": "Admin Interface"},
    {"app": "auth", "models": ("auth.User", "auth.Group")},
    {"app": "members", "label": "Members", "models": ("members.Members",)},
    {"app": "userlog", "label": "User Log", "models": ("userlog.UserLog",)},
    {
        "app": "buildings",
        "label": "Buildings",
        "models": (
            "buildings.Department",
            "buildings.Building",
            "buildings.Block",
            "buildings.Floor",
            "buildings.RoomType",
            "buildings.Room",
            "buildings.Item",
            "buildings.Maintenance",
            "buildings.Ticket",
            "buildings.Activity",
            "buildings.ItemSwap",
            "buildings.Assignee",
        ),
    },
)
# Password validation

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

LANGUAGE_CODE = "en-us"

TIME_ZONE = "Asia/Kolkata"

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)

MEDIA_URL = "/media/"
# MEDIA_ROOT = os.path.join(BASE_DIR, "images")

MEDIA_ROOT = "/www/app/media/"

# STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")

STATIC_ROOT = "/www/app/staticfiles/"

STATIC_URL = "/static/"

STASTATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]


## Setup HUEY

HUEY = {
    "huey_class": "huey.RedisHuey",  # Huey implementation to use.
    "name": env.str("DJANGO_NAME", default="ims"),  # Use db name as huey name
    "connection": {
        "host": "redis",
        "port": 6379,
    },  # Read timeout in seconds, use float for fractions of a second.
    "consumer": {
        "workers": 4,
        "blocking": True,
        "loglevel": logging.INFO,
    },
}

if DEBUG:
    HUEY["immediate_use_memory"] = False
    HUEY["immediate"] = False


## AUTO_FIELD settings
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# ## Cron jobs for maintenance check
# CRONJOBS = [
#     ## Every day at 4:00 a.m maintenance check
#     ("* 4 * * *", "django.core.management.call_command", ["check_maintenance"]),
# ]

## Security settings

if not DEBUG:
    SECURE_SSL_REDIRECT = True
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_HSTS_SECONDS = 31536000  # 1 year
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SECURE_BROWSER_XSS_FILTER = True
    X_FRAME_OPTIONS = "DENY"
    ALLOWED_HOSTS = ["*"]
