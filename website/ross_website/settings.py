"""
Django settings for ross_website project.

Generated by 'django-admin startproject' using Django 2.0.4.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""

import os
from .test_secret import secret_key, debug_state, hosts
#from .secret import secret_key, debug_state, hosts
import django_heroku

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = secret_key()

# for git
# SECRET_KEY = "wlkv5(r&n4%-08pg-(f-$0w+-rk-*7#g#i0q4jmgkh_mqh=0tt"

DEBUG = debug_state()
ALLOWED_HOSTS = hosts()

# Application definition

INSTALLED_APPS = [
    'whitenoise.runserver_nostatic',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'homepage',
    'blog',
    'data_vis',

]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    
]

ROOT_URLCONF = 'ross_website.urls'

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
]

WSGI_APPLICATION = 'ross_website.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

# ##### This is for the AWS RDS DB
# if 'RDS_HOSTNAME' in os.environ:
#      DATABASES = {
#          'default': {
#              'ENGINE': 'django.db.backends.mysql',
#              'NAME': os.environ['RDS_DB_NAME'],
#              'USER': os.environ['RDS_USERNAME'],
#              'PASSWORD': os.environ['RDS_PASSWORD'],
#              'HOST': os.environ['RDS_HOSTNAME'],
#              'PORT': os.environ['RDS_PORT'],
#          }
#      }


# This is for a local postgres test db in a Docker container.
if not DEBUG:
     DATABASES = {
          'default': {
              'ENGINE': 'django.db.backends.postgresql_psycopg2',
              'NAME': 'postgres',
              'USER': 'postgres',
              'HOST': 'db', # set in docker-compose.yml
              'PORT': 5432 # default postgres port
          }
         }
else: 
    # Activate Django-Heroku.
    django_heroku.settings(locals())

# # Built in DB
#      DATABASES = {
#           'default': {
#               'ENGINE': 'django.db.backends.sqlite3',
#               'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#           }
#          }


# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'GMT'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'

#TODO update on deplotyment. 

PROJECT_ROOT = os.path.realpath(os.path.dirname(__file__))

if DEBUG:
    MEDIA_ROOT = 'media'
    MEDIA_URL = 'media/'
    STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
    
else:
    MEDIA_ROOT = 'media'
    MEDIA_URL = 'media/'
    STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
#    '/var/www/static/',
]

# STATICFILES_DIRS = [
#     os.path.join(BASE_DIR, 'static_build')
# ]


