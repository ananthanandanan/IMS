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

from collections import OrderedDict


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "czif=j6p5yagrslg#(1axv35%#-+_x02fff=kzg06r3lc*8i*9"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

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
    "easy_select2",
    "django_crontab",
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


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

## Sqlite3 for development

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

## Uncomment the following lines if you are using postgresql

# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.postgresql",
#         "NAME": os.environ.get("POSTGRES_NAME"),
#         "USER": os.environ.get("POSTGRES_USER"),
#         "PASSWORD": os.environ.get("POSTGRES_PASSWORD"),
#         "HOST": "db",
#         "PORT": "5432",

#     }
# }

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
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "Asia/Kolkata"

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

MEDIA_URL = "/logo/"
MEDIA_ROOT = os.path.join(BASE_DIR, "admin-interface/logo/")
MEDIA_URL1 = "members/agent/"
MEDIA_ROOT1 = os.path.join(BASE_DIR, "templates/agent/")

MEDIA_URL2 = "members/customer/"
MEDIA_ROOT2 = os.path.join(BASE_DIR, "templates/customer/")

STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
STATIC_URL = "/static/"

STASTATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]


CRONJOBS = [
    ## Every day at 4:00 a.m maintenance check
    ("* 4 * * *", "django.core.management.call_command", ["check_maintenance"]),
]

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
