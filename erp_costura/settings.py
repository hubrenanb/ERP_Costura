"""
Django settings for erp_costura project.
"""

from pathlib import Path
import os
from dotenv import load_dotenv
import dj_database_url

# Carrega variáveis do arquivo .env localmente
load_dotenv()

# Caminho base do projeto
BASE_DIR = Path(__file__).resolve().parent.parent

# SEGURANÇA: Chave secreta vinda do ambiente ou fallback para desenvolvimento
SECRET_KEY = os.getenv('SECRET_KEY', 'django-insecure-chave-padrao-local-apenas')

# SEGURANÇA: Debug False em produção, True em desenvolvimento
DEBUG = os.getenv('DEBUG', 'True') == 'True'

# Configuração de domínios permitidos
ALLOWED_HOSTS = os.getenv('DOMINIOS_PERMITIDOS', '127.0.0.1,localhost').split(',')

# Definição dos Apps
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Apps do ERP Ckaizen
    'core',
    'estoque',
    'producao',
    'financeiro',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    # WhiteNoise para servir arquivos estáticos de forma eficiente
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'erp_costura.urls'

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

WSGI_APPLICATION = 'erp_costura.wsgi.application'

# BANCO DE DADOS: PostgreSQL na nuvem ou SQLite local
DATABASES = {
    'default': dj_database_url.config(
        default=os.getenv('DATABASE_URL', f'sqlite:///{BASE_DIR / "db.sqlite3"}'),
        conn_max_age=600,
        conn_health_checks=True,
    )
}

# Validação de senhas
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Internacionalização
LANGUAGE_CODE = 'pt-br'
TIME_ZONE = 'America/Sao_Paulo'
USE_I18N = True
USE_TZ = True

# Arquivos Estáticos (CSS, JavaScript, Imagens)
STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Configuração do WhiteNoise para compressão e cache de estáticos
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Modelo de Usuário Personalizado
AUTH_USER_MODEL = 'core.Usuario'

# Rotas de Autenticação
LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'listar_comandas'
LOGOUT_REDIRECT_URL = 'login'

# Configuração de campos de ID padrão
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'