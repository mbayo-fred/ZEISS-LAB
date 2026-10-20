"""
Django settings for zeiss_medical_diagnostic_laboratory project.
Zeiss Medical Diagnostic Laboratories — Laboratory Information System (LIS)
"""

import os
import dj_database_url
from pathlib import Path

# --------------------------------------------------------------------------
# Paths
# --------------------------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent

# --------------------------------------------------------------------------
# Security
# --------------------------------------------------------------------------
# Use Render's Environment Variable for SECRET_KEY. Fallback for local dev.
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-_#l3=5eeor$)c2$*z_g8u*@%j%)(e42!7@3mbhh3hb*pe2)d^w')

# Use Render's Environment Variable for DEBUG. Fallback is True for local dev.
DEBUG = os.environ.get('DEBUG', 'True') == 'True'

# Allow Render's URL and localhost
ALLOWED_HOSTS = ['*'] # You can restrict this later to your specific Render URL

# CSRF Trusted Origins (Required for POST requests on Render)
CSRF_TRUSTED_ORIGINS = [
    'https://*.onrender.com',
    'http://localhost',
    'http://127.0.0.1',
]

# --------------------------------------------------------------------------
# Applications
# --------------------------------------------------------------------------
INSTALLED_APPS = [
    # Django contrib
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Third-party
    'rest_framework',
    'crispy_forms',

    # Local apps — Zeiss LIS
    'core',
    'patients',
    'laboratory',
    'reports',
    'inventory',
]

# --------------------------------------------------------------------------
# Middleware
# --------------------------------------------------------------------------
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware', # ADDED FOR RENDER STATIC FILES
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'zeiss_medical_diagnostic_laboratory.urls'

# --------------------------------------------------------------------------
# Templates
# --------------------------------------------------------------------------
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'zeiss_medical_diagnostic_laboratory.wsgi.application'

# --------------------------------------------------------------------------
# Database
# --------------------------------------------------------------------------
# This logic safely handles the SQLite path for local development (Windows/Mac) 
# while allowing Render to use the Supabase DATABASE_URL environment variable.
SQLITE_PATH = str(BASE_DIR).replace('\\', '/') + '/db.sqlite3'

DATABASES = {
    'default': dj_database_url.config(
        default=f"sqlite:///{SQLITE_PATH}",
        conn_max_age=600
    )
}

# --------------------------------------------------------------------------
# Authentication
# --------------------------------------------------------------------------
AUTH_USER_MODEL = 'core.User'

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'dashboard'
LOGOUT_REDIRECT_URL = 'login'

# --------------------------------------------------------------------------
# Internationalization
# --------------------------------------------------------------------------
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Africa/Kampala'
USE_I18N = True
USE_TZ = True

# --------------------------------------------------------------------------
# Static & Media files
# --------------------------------------------------------------------------
STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

# ADDED FOR RENDER: Compresses static files for faster loading
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# --------------------------------------------------------------------------
# Default primary key
# --------------------------------------------------------------------------
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# --------------------------------------------------------------------------
# Crispy forms
# --------------------------------------------------------------------------
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"

# --------------------------------------------------------------------------
# REST Framework
# --------------------------------------------------------------------------
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 25,
}

# --------------------------------------------------------------------------
# Email (Gmail SMTP)
# --------------------------------------------------------------------------
# Use Render's Environment Variables for Email Passwords
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER', 'mbayofred37@gmail.com')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD', 'xxxx xxxx xxxx xxxx') # App Password
DEFAULT_FROM_EMAIL = 'Zeiss Medical Diagnostic Laboratories <mbayofred37@gmail.com>'

# --------------------------------------------------------------------------
# Zeiss LIS — custom project settings
# --------------------------------------------------------------------------
ZEISS_LAB_NAME = "Zeiss Medical Diagnostic Laboratories"
ZEISS_LAB_SHORT = "ZMDL"
ZEISS_LAB_ADDRESS = "Kampala, Uganda"
ZEISS_LAB_PHONE = "+256 000 000 000"
ZEISS_LAB_EMAIL = "info@zeisslab.local"
ZEISS_PATIENT_ID_PREFIX = "ZMD"
ZEISS_ORDER_ID_PREFIX = "ORD"
