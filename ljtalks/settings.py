"""
Django settings for ljtalks project.

Generated by 'django-admin startproject' using Django 4.2.16.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from pathlib import Path
import os
# import sys
# from django.contrib.messages import constants as messages
import dj_database_url
if os.path.isfile('env.py'):
    import env
import cloudinary
import cloudinary.uploader
import cloudinary.api


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# if os.path.isfile("env.py"):
#     DEBUG = True
# else:
#     DEBUG = False

ALLOWED_HOSTS = [
    '.codeinstitute-ide.net', '.herokuapp.com']

CSRF_TRUSTED_ORIGINS = [
    "https://*.codeinstitute-ide.net/",
    "https://*.herokuapp.com"
]

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    # Statics; should be before apps that manage static files
    'django.contrib.staticfiles',
    'django.contrib.sites',  # anywhere for multiple
    # sites & django-allauth integration
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'django_summernote',  # Rich text editor for admin
    'cloudinary_storage',
    'cloudinary',  # Image mgmnt. After cloudinary_storage
    # 'crispy_forms',
    # 'crispy_bootstrap5',
    'blog',  # Custom apps after django then third-party apps
    'ytapi',
    # 'services',
    # 'booking',
]

# CRISPY_ALLOWED_TEMPLATE_PACKs = 'bootstrap5'
# CRISPY_TEMPLATE_PACK = 'bootstrap5'

# Site framework ID - required for django.contrib.sites
SITE_ID = 1  # Django can handle multiple sites from one db
LOGIN_REDIRECT_URL = '/'  # returns user to home page after login
LOGOUT_REDIRECT_URL = '/'  # returns user to home page after logout
# ACCOUNT_SIGNUP_REDIRECT_URL = '/'  # Unless redirected with Next

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # additional functionality to the projects account user authentication
    'allauth.account.middleware.AccountMiddleware',
]

ROOT_URLCONF = 'ljtalks.urls'

TEMPLATES_DIR = os.path.join(BASE_DIR, 'templates')

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATES_DIR],
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

WSGI_APPLICATION = 'ljtalks.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

DATABASES = {
    'default':
    dj_database_url.parse(os.environ.get("DATABASE_URL"))
}

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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

ACCOUNT_EMAIL_VERIFICATION = 'mandatory'  # We def want this
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_AUTHENTICATION_METHOD = 'username_email'  # Login with email/username
# (again CHATGPT down below)
ACCOUNT_USERNAME_REQUIRED = True  # We want usernames


# BEWARE ChatGpt asked me to add this when adding auth and email verification
AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
)

# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

# MESSAGE_TAGS = {
#     messages.SUCCESS: "alert-success",
#     messages.ERROR: "alert-danger",
# }

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')  # for collectstatic

# Configure Whitenoise to handle static files
# STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'

# Media file handling (Images and uploads)
# MEDIA_URL = '/media/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
