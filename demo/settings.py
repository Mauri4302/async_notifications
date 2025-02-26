"""
Django settings for demo project.

Generated by 'django-admin startproject' using Django 2.1.5.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""
import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'l(*i&mt+z=zcf!nk4)y=2n=$(pba1yz6#n4mtci5lqw%y3%f9e'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'async_notifications',
    'ckeditor',
    'markitup',
    'markdown',
    'django_celery_beat',
    'django_celery_results'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'demo.urls'

# ASYNC_TEMPLATES_NOTIFICATION = os.path.abspath(os.path.join(BASE_DIR, 'templates'))

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

WSGI_APPLICATION = 'demo.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'America/Costa_Rica'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

STATIC_URL = '/static/'



CELERY_MODULE = "demo.celery"
CELERY_TIMEZONE = TIME_ZONE
CELERY_ACCEPT_CONTENT = ['pickle', 'json']
# CELERY_ACCEPT_CONTENT = ['json']

'''
Variables de entorno para acceder a mailhog y hacer pruebas
'''
'''EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'localhost'
EMAIL_PORT = 1025 '''

DEFAULT_FROM_EMAIL = "mail@example.com"
EMAIL_HOST = "localhost"
EMAIL_PORT = 1025
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST = 'localhost'
# EMAIL_PORT = 1025

ASYNC_NOTIFICATION_TEXT_AREA_WIDGET = 'ckeditor.widgets.CKEditorWidget'
ASYNC_NEWSLETTER_WIDGET = 'markitup.widgets.AdminMarkItUpWidget'
MARKITUP_FILTER = ('markdown.markdown', {'safe_mode': True})
ASYNC_NEWS_BASE_MODELS = {
    'async_notifications.EmailNotification': ['async_notifications.EmailNotification', 'Emails', 'demo.forms.EmailExampleForm'],
}

# docker run -d --rm --name  redis -p 6379:6379 -d redis
# pip install redis
# CELERY_BROKER_URL =  'redis://localhost:6379/0'
CELERY_BROKER_URL = 'amqp://guest:guest@localhost:5672//'
# CELERY_BROKER_URL = 'amqp://guest:guest@demo-rabbitmq:5672//'
# BROKER_URL = 'amqp://guest:guest@demo-rabbitmq:5672//'
# CELERY_RESULT_BACKEND = 'django-db'
# with rabbitmq
# service rabbitmq-server start

ASYNC_BCC = 'ejemplo@luisza.com'
ASYNC_CC = 'ejemplo@luisza.com,ejemplo2@luisza.com'

MARKITUP_SET = 'markitup/sets/markdown/'

ASYNC_NEWSLETTER_HEADER = {'Reply-To': 'contact@example.com'}
