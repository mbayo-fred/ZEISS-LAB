"""
Django settings for zeiss_medical_diagnostic_laboratory project.
Zeiss Medical Diagnostic Laboratories — Laboratory Information System (LIS)
"""

from pathlib import Path

# --------------------------------------------------------------------------
# Paths
# --------------------------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent


# --------------------------------------------------------------------------
# Security
# --------------------------------------------------------------------------
SECRET_KEY = 'django-insecure-_#l3=5eeor$)c2$*z_g8u*@%j%)(e42!7@3mbhh3hb*pe2)d^w'

DEBUG = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1']


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
]


# --------------------------------------------------------------------------
# Middleware
# --------------------------------------------------------------------------
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
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
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
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

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'


# --------------------------------------------------------------------------
# Default primary key
# --------------------------------------------------------------------------
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# --------------------------------------------------------------------------
# Crispy forms (Bootstrap 5 via crispy_forms built-in pack)
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
# Email (console backend for development)
# --------------------------------------------------------------------------
# Email Configuration (Gmail)
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'mbayofred37@gmail.com'  # Your Gmail address
EMAIL_HOST_PASSWORD = 'xxxx xxxx xxxx xxxx'  # Your 16-letter Google App Password
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
