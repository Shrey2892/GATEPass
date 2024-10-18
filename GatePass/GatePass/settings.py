"""
Django settings for GatePass project.

Generated by 'django-admin startproject' using Django 5.1.2.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

from pathlib import Path         #pip install --upgrade pip setuptools wheel : FOR WHEEL BUILD ERROR
import os
# import pymysql
# pymysql.install_as_MySQLdb()
SESSION_ENGINE = 'django.contrib.sessions.backends.cache'
from mongoengine import connect
SESSION_EXPIRE_AT_BROWSER_CLOSE = True  # Expire session when the browser is closed

# MONGODB_NAME = 'User'
# MONGODB_HOST = 'localhost'  # or your MongoDB host
# MONGODB_PORT = 27017         # default MongoDB port
MONGODB_USER = 'admin'  # if using authentication
MONGODB_PASSWORD = 'Shreya123'  # if using authentication
#Connect to your MongoDB database
connect(
    db ='User',  # replace with your database name
    host='localhost',         # replace with your MongoDB host
    port=27017 ,
    username = 'admin',
    password = 'Shreya123',
                                # default MongoDB port
)

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-3%fr9(@1i=hii4pactsh!5^pq%p9nzyt7%8h7@oxleqcx5(#!3'

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
    'App',
    'rest_framework',
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

ROOT_URLCONF = 'GatePass.urls'

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

WSGI_APPLICATION = 'GatePass.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

# DATABASES = {
#     'default': {

        # 'ENGINE': 'django.db.backends.mongoengine',  # Specifies the database engine
# # #         # 'NAME': BASE_DIR / "db.sqlite3",      

#         'ENGINE': 'django.db.backends.dummy',
#         'NAME': 'User',
#         'USER': 'admin',
#         'PASSWORD': 'Shreya123',
#         'HOST': 'localhost',  # Use '127.0.0.1' or your server's IP
#         'OPTIONS': {
#             'authSource': 'admin',  # if your user is in the admin db
#         }
        
#     }
# }


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = 'static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'App/templates/static'), # Adjust this path if your static files are located elsewhere
]

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'



LOGIN_URL = '/login/'  # Adjust to match your login URL
LOGIN_REDIRECT_URL = '/home/'  # Redirect after login