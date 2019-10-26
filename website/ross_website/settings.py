import os

"""
Django settings for ross_website project.

Generated by 'django-admin startproject' using Django 2.0.4.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ['SECRET_KEY'] 

DEBUG = ''
#SECURE_SSL_REDIRECT = ''
SESSION_COOKIE_SECURE = ''
CSRF_COOKIE_SECURE = ''

if os.environ['DEBUG'] == 'False':
    DEBUG = False
    #SECURE_SSL_REDIRECT = False
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True

    
elif os.environ['DEBUG'] == 'True':
    DEBUG = True
    SECURE_SSL_REDIRECT = False
    SESSION_COOKIE_SECURE = False
    CSRF_COOKIE_SECURE = False

ALLOWED_HOSTS = [i for i in os.environ['ALLOWED_HOSTS'].split('|')]
# Application definition

INSTALLED_APPS = [
    #'whitenoise.runserver_nostatic',
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

# This is for a local postgres test db in a Docker container.

# Note: if the postgres data is not "in-sync" (also the user and pass)
# this may cause errors as the DB cannot be accessed


if DEBUG:
    DATABASES = {
        'default': {
            'ENGINE': os.environ['DBENGINE'],
            'NAME': os.environ['DATABASE'],
            'USER': os.environ['DB_USER'],
            'PASSWORD': os.environ['DB_PASS'],
            'HOST': os.environ['SQL_HOST'], # set in docker-compose.yml
            'PORT': os.environ['DB_PORT'], # default postgres port
            }
        }
else: 
    DATABASES = {
        'default': {
            'ENGINE': os.environ['DBENGINE'],
            'NAME': os.environ['DATABASE'],
            'USER': os.environ['DB_USER'],
            'PASSWORD': os.environ['DB_PASS'],
            'HOST': os.environ['SQL_HOST'], # set in docker-compose.yml
            'PORT': os.environ['DB_PORT'], # default postgres port
            }
        }


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

PROJECT_ROOT = os.path.realpath(os.path.dirname(__file__))
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles') 
STATIC_URL = '/static/'

if DEBUG:
    MEDIA_ROOT = 'media'
    MEDIA_URL = 'media/'    # STATIC_ROOT = os.path.join(BASE_DIR, 'static')    
    
else:
    MEDIA_ROOT = 'media'
    MEDIA_URL = 'media/'
    # heroku specific
    # STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "local_static"),
#    '/var/www/static/',
]

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
