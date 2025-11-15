import os
from pathlib import Path
from datetime import timedelta

# ===============================
# 📁 Caminhos base
# ===============================
BASE_DIR = Path(__file__).resolve().parent.parent

# ===============================
# 🔐 Segurança
# ===============================
SECRET_KEY = 'django-insecure-sua-chave-secreta-aqui'
DEBUG = True
ALLOWED_HOSTS = ["*"]

# ===============================
# 📦 Aplicativos instalados
# ===============================
INSTALLED_APPS = [
    # Apps Django padrão
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Terceiros
    'rest_framework',
    'rest_framework.authtoken',
    'rest_framework_simplejwt.token_blacklist',
    'corsheaders',

    # Apps locais
    'users',
    'books',
    'catalog',
    'loans',
]

# ===============================
# ⚙️ Middleware
# ===============================
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',  # deve vir antes de CommonMiddleware
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# ===============================
# 🔗 URLs e Templates
# ===============================
ROOT_URLCONF = 'biblioteca.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

WSGI_APPLICATION = 'biblioteca.wsgi.application'

# ===============================
# 🗄️ Banco de dados
# ===============================
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'biblioteca_db',
        'USER': 'biblioteca_user',
        'PASSWORD': 'Marjosa78!',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}

# ===============================
# 👥 Autenticação e Usuários
# ===============================
AUTH_USER_MODEL = 'users.User'

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# ===============================
# 🌍 Internacionalização
# ===============================
LANGUAGE_CODE = 'pt-br'
TIME_ZONE = 'America/Sao_Paulo'
USE_I18N = True
USE_TZ = True

# ===============================
# 📁 Arquivos estáticos e mídia
# ===============================
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'static']

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# ===============================
# 🔐 Django REST + JWT
# ===============================
REST_FRAMEWORK = {
    # ✅ Usa autenticação via JWT
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),

    # ✅ Exige autenticação por padrão
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),

    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
}

# ===============================
# 🔑 Configuração do JWT
# ===============================
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': True,
    'AUTH_HEADER_TYPES': ('Bearer',),
    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
}

# ===============================
# 🌐 CORS (para o frontend React)
# ===============================
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

# ✅ Permite envio de cookies e headers de autenticação
CORS_ALLOW_CREDENTIALS = True

# 🔧 (opcional) se quiser liberar tudo durante testes:
# CORS_ALLOW_ALL_ORIGINS = True

# ===============================
# 🔧 Padrão do campo ID
# ===============================
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
