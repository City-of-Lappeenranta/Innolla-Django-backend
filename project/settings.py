# -*- coding: utf-8 -*-
#
# Copyright Haltu Oy, info@haltu.fi
# All rights reserved.
#

import os
BASEDIR = os.path.dirname(os.path.abspath(__file__))

#
# Core configuration
#

BASEDIR = os.path.dirname(os.path.abspath(__file__))

SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', '')

ALLOWED_HOSTS = []

ROOT_URLCONF = 'project.urls'

INSTALLED_APPS = [
  'innolla',
  'graphene_django',
  'corsheaders',

  'health_check',
  'health_check.db',
  'health_check.cache',
  'health_check.storage',

  'django.contrib.admin',
  'django.contrib.auth',
  'django.contrib.contenttypes',
  'django.contrib.humanize',
  'django.contrib.sessions',
  'django.contrib.messages',
  'django.contrib.staticfiles',
]

MIDDLEWARE = [
  'django.middleware.security.SecurityMiddleware',
  'django.middleware.gzip.GZipMiddleware',
  'django.contrib.sessions.middleware.SessionMiddleware',
  'corsheaders.middleware.CorsMiddleware',
  'django.middleware.common.CommonMiddleware',
  'django.middleware.csrf.CsrfViewMiddleware',
  'django.contrib.auth.middleware.AuthenticationMiddleware',
  'django.contrib.messages.middleware.MessageMiddleware',
  'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

TEMPLATES = [
  {
    'BACKEND': 'django.template.backends.django.DjangoTemplates',
    'DIRS': [os.path.join(BASEDIR, 'templates')],
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

WSGI_APPLICATION = 'project.wsgi.application'

# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')


#
# Database
#

# Comes from local_settings


#
# Password validation
#

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


#
# Internationalization
#

LANGUAGE_CODE = 'en'

LANGUAGES = (
  ('en', 'English'),
)

LOCALE_PATHS = (
  os.path.join(BASEDIR, 'locale'),
)

TIME_ZONE = 'Europe/Helsinki'

USE_I18N = True

USE_L10N = True

USE_TZ = True


#
# Static files
#

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASEDIR, '..', 'staticroot')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
STATICFILES_DIRS = (
  os.path.join(BASEDIR, 'static'),
)

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASEDIR, '..', 'mediaroot')

#
# Graphene
#

GRAPHENE = {
  'SCHEMA': 'innolla.schema.schema',
  'SCHEMA_OUTPUT': 'data/schema.json',
  'SCHEMA_INDENT': 2,
  'MIDDLEWARE': [
    'graphql_jwt.middleware.JSONWebTokenMiddleware',
  ],
  }


AUTHENTICATION_BACKENDS = [
    'graphql_jwt.backends.JSONWebTokenBackend',
    'django.contrib.auth.backends.ModelBackend',
]

# vim: tabstop=2 expandtab shiftwidth=2 softtabstop=2
