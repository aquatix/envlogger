"""
Django settings for envlogger project.

Generated by 'django-admin startproject' using Django 1.11.2.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
try:
    SECRET_KEY = os.environ['ENVLOGGER_SECRET_KEY']
except KeyError:
    print('No ENV var found for ENVLOGGER_SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False
try:
    DEBUG = os.environ['DEBUG']
except KeyError:
    DEBUG = False

DEBUGTOOLBAR = False
#if DEBUG:
#    DEBUGTOOLBAR = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1', '[::1]']
try:
    ALLOWED_HOSTS.append(os.environ['ENVLOGGER_SERVER_HOST'])
except KeyError:
    print('No ENV var found for ENVLOGGER_SERVER_HOST')

if DEBUGTOOLBAR:
    INTERNAL_IPS = ['127.0.0.1']

# Application definition

INSTALLED_APPS = [
    'energy',
    'fuel',
    'temperature',
    'weather',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

if DEBUGTOOLBAR:
    INSTALLED_APPS.append('debug_toolbar')

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

if DEBUGTOOLBAR:
    MIDDLEWARE.append('debug_toolbar.middleware.DebugToolbarMiddleware')

ROOT_URLCONF = 'envlogger.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
    #{
    #    'BACKEND': 'django.template.backends.jinja2.Jinja2',
    #    'DIRS': [],
    #    'APP_DIRS': True,
    #    'OPTIONS': {
    #    },
    #},
]

WSGI_APPLICATION = 'envlogger.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

try:
    DATABASES['default'] = {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ['ENVLOGGER_DB_NAME'],
        'USER': os.environ['ENVLOGGER_DB_USER'],
        'PASSWORD': os.environ['ENVLOGGER_DB_PASS'],
        'HOST': os.environ['ENVLOGGER_DB_HOST'],
        'PORT': os.environ['ENVLOGGER_DB_PORT'],
        #
    }
except KeyError as e:
    print('No ENV var for DB config found: {}'.format(e))


# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'
try:
    TIME_ZONE = os.environ['ENVLOGGER_TIME_ZONE']
except KeyError:
    print('No ENV var found for ENVLOGGER_TIME_ZONE')

USE_I18N = True

USE_L10N = True

USE_TZ = True

DATETIME_FORMAT = '%Y-%m-%d %H:%M'
try:
    DATETIME_FORMAT = os.environ['ENVLOGGER_DATETIME_FORMAT']
except KeyError:
    print('No ENV var found for ENVLOGGER_DATETIME_FORMAT')


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_URL = '/static/'
try:
    STATIC_ROOT = os.environ['ENVLOGGER_STATIC_ROOT']
except KeyError:
    print('No ENV var found for ENVLOGGER_STATIC_ROOT')

SITE_TITLE = 'envlogger'
try:
    SITE_TITLE = os.environ['ENVLOGGER_SITE_TITLE']
except KeyError:
    print('No ENV var found for ENVLOGGER_SITE_TITLE')
