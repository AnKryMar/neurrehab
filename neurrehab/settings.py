import os
from pathlib import Path
from django.utils.translation import gettext_lazy as _
import warnings

# Отключение предупреждений TensorFlow
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

# Отключение oneDNN custom operations
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

# Отключение предупреждений от diffusers
warnings.filterwarnings("ignore", category=FutureWarning, module="diffusers")

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
MEDIA_ROOT = BASE_DIR / 'media'
MEDIA_URL = '/media/'

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-5%g8jna7)dtk52c@+69h5@6jz-iu=br83qc2f_a2^7!w&zi5p-'

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
    # Новые приложения
    'accounts',
    'tasks',
    'ai',
    'core',
    'main',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.locale.LocaleMiddleware',
]

ROOT_URLCONF = 'neurrehab.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR / 'templates',  # Использование объекта Path для директории шаблонов
            BASE_DIR / 'main' / 'templates',  # Путь к шаблонам в приложении main
        ],
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

WSGI_APPLICATION = 'neurrehab.wsgi.application'

# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGES = [
    ('ru', _('Russian')),
    ('en', _('English')),
]

LANGUAGE_CODE = 'ru'

TIME_ZONE = 'UTC'

USE_I18N = True
USE_L10N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOCALE_PATHS = [
    BASE_DIR / 'locale',
]

LOGIN_REDIRECT_URL = 'profile'
LOGOUT_REDIRECT_URL = 'home'

SESSION_ENGINE = 'django.contrib.sessions.backends.db'  # Используйте базу данных для хранения сессий
SESSION_COOKIE_SECURE = False  # Убедитесь, что для локальной разработки это выключено
SESSION_EXPIRE_AT_BROWSER_CLOSE = False  # Сессия не истекает при закрытии браузера
AUTH_USER_MODEL = 'accounts.CustomUser'

# Добавьте ваш API-ключ ProxyAPI
HUGGING_FACE_API_KEY = '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'