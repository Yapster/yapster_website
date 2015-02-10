"""
Django settings for yapster_website project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '2)r)5eat&%beb)kiv)hq#eb=2b%9q2daf=^q9o6$!39cq&bkms'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []

EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = '587'
EMAIL_HOST_USER = 'chris@yapsterapp.com'
EMAIL_HOST_PASSWORD = 'Yapster1234'
EMAIL_SUBJECT_PREFIX = '[CONTACTS]'

AWS_ACCESS_KEY_ID = 'AKIAJ2WIFTVZMGME4V4A'
AWS_SECRET_ACCESS_KEY = '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'


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'pydub',
    'home',
    'main_app'
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'yapster_website.urls'

WSGI_APPLICATION = 'yapster_website.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        },
    # 'ye_1_db_1': {
    #     'NAME': 'ye_1_db_1',
    #     'ENGINE': 'django.contrib.gis.db.backends.postgis',
    #     'USER': 'yapster',
    #     'PASSWORD': 'Yapster1000000000',
    #     'HOST': 'ye-1-db-1.cagmlb1zwzjw.us-east-1.rds.amazonaws.com',
    #     'PORT': '5432',
    #     }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/assets/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'assets/'),
)

TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, 'templates'),
)

GEOS_LIBRARY_PATH = 'C:/OSGeo4W/bin/geos_c.dll'
