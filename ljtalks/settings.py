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
# Load environment variables in Gitpod
if os.path.isfile('env.py'):
    import env
import cloudinary
import cloudinary.uploader
import cloudinary.api


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# Secret Key
SECRET_KEY = os.environ.get("SECRET_KEY")

# Set debug based on env.py presence
if os.path.isfile("env.py"):
    DEBUG = True
else:
    DEBUG = False

# Development or Production Environment 
# # Switch to production manually for updates
# # DATABASE_URL = os.environ.get('development')  # trade
# DATABASE_URL = os.environ.get('production')  # bush
# Toggle this line in Gitpod when needed
# DATABASES['default'] = (dj_database_url.parse(os.environ.get("DEV_DATABASE_URL")))
# Gitpod-specific override for DEV_DATABASE_URL
# if os.getenv("USE_DEV_DB") == "True" and "GITPOD_WORKSPACE_URL" in os.environ:
#     DATABASES['default'] = dj_database_url.parse(os.environ.get("DEV_DATABASE_URL"))


ALLOWED_HOSTS = [
    '.codeinstitute-ide.net',
    'ljtalksdev-61ea4d3e9223.herokuapp.com',
    'ljblogs-fcdcaa00fdda.herokuapp.com',
    'ljtalks.com',
    'www.ljtalks.com'
]

CSRF_TRUSTED_ORIGINS = [
    "https://ljtalksdev-61ea4d3e9223.herokuapp.com",
    "https://ljblogs-fcdcaa00fdda.herokuapp.com",
    "https://ljtalks.com",
    "https://www.ljtalks.com",
    "https://*.codeinstitute-ide.net"
]

# Database configuration (development v production)
DATABASES = {
    'default': dj_database_url.parse(
        os.environ.get(
            "DATABASE_URL"))
}
DATABASE_NAME = "Production Database"


# Set Database name for base template
def database_context(request):
    from django.conf import settings
    return {'DATABASE_NAME': settings.DATABASE_NAME}


# Uncomment this group in Gitpod to switch to the development database
DATABASES['default'] = dj_database_url.parse(os.environ.get(
    "DEV_DATABASE_URL"))
DATABASE_NAME = "Development Database"
print(f"Connected to: {DATABASE_NAME}")


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
    'django_summernote',
    'captcha',
    'cloudinary_storage',
    'cloudinary',  # Image mgmnt. After cloudinary_storage
    'crispy_forms',
    'crispy_bootstrap5',
    'blog',  # Custom apps after django then third-party apps
    'emails',
    'ljtalks',
    'ytapi',
    # 'services',
    # 'booking',
]

CRISPY_ALLOWED_TEMPLATE_PACKS = 'bootstrap5'
CRISPY_TEMPLATE_PACK = 'bootstrap5'

# Site framework ID - required for django.contrib.sites
# Django can handle multiple sites from one db
SITE_ID = 1  # Production
SITE_ID = 2  # Development/staging

LOGIN_REDIRECT_URL = '/'  # returns user to home page after login
LOGOUT_REDIRECT_URL = '/'  # returns user to home page after logout
# ACCOUNT_SIGNUP_REDIRECT_URL = '/'  # Unless redirected with Next
ACCOUNT_FORMS = {
    'signup': 'ljtalks.forms.CustomSignupForm',
}

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

# Set up email configurations
if DEBUG:
    EMAIL_BACKEND = 'django.core.backends.console.EmailBackend'
# For testing locally
else:
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

# you can use Django’s console backend for development (this will print the
# email content to the terminal instead of sending it)
# Use console email backend for development
# With this, any emails will appear in your terminal instead of attempting
# to send them, which avoids connection issues during development.
EMAIL_HOST = 'smtp.privateemail.com'
EMAIL_PORT = 465
EMAIL_USE_SSL = True
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = os.getenv('EMAIL_HOST_USER')  # This can remain as your email


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
                # Chat GPT's idea
                # base nav to show additional options to different groups
                'ljtalks.context_processors.add_is_tester',
                'ljtalks.context_processors.recaptcha_key',
                'ljtalks.settings.database_context',
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

# For recaptcha
ACCOUNT_ADAPTER = 'ljtalks.adapters.CustomAccountAdapter'

ACCOUNT_EMAIL_VERIFICATION = 'mandatory'  # We def want this
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_CONFIRMATION_EMAIL = True
ACCOUNT_AUTHENTICATION_METHOD = 'username_email'  # Login with email/username
# (again CHATGPT down below)
ACCOUNT_USERNAME_REQUIRED = True  # We want usernames

# Optional: Prevent login until email is verified
ACCOUNT_LOGIN_ON_EMAIL_CONFIRMATION = False

# Will this stop the emails coming from example@ 
ACCOUNT_EMAIL_SUBJECT_PREFIX = "LJ Talks "  # Customize the prefix
DEFAULT_FROM_EMAIL = os.getenv("DEFAULT_FROM_EMAIL")  # Set the default email


# BEWARE ChatGpt asked me to add this when adding auth and email verification
AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
)

# Adding this for debugging nav group status
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
        },
    },
}

# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

# Custom date and time formats
DATE_FORMAT = 'd/m/Y'
TIME_FORMAT = 'H:i'
DATETIME_FORMAT = 'd/m/Y H:i'

# MESSAGE_TAGS = {
#     messages.SUCCESS: "alert-success",
#     messages.ERROR: "alert-danger",
# }

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
# Is this the line that broke it?
STATIC_ROOT = BASE_DIR / 'staticfiles'  # for collectstatic
# This is previous. It didn't help yet so this may need reverting.
# STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')  # for collectstatic

DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'

# Recaptcha and other API keys
RECAPTCHA_PRIVATE_KEY = os.environ.get("RECAPTCHA_PRIVATE_KEY")
RECAPTCHA_SITE_KEY = os.environ.get("RECAPTCHA_SITE_KEY")


# Configure Whitenoise to handle static files
# this is for Django versions olderthan 4.2
# STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
# for Django 4.2+

# This from whitenoise docs throws settings_ALLOWED_HOSTS error
# STORAGES = {
#     "staticfiles": {
#         "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
#     },
# }

# Media file handling (Images and uploads)
# MEDIA_URL = '/media/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
