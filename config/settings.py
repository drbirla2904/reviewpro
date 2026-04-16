from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent

# ── Load .env file automatically ──────────────────────────────────────────────
# Runs once. python-dotenv reads .env and populates os.environ.
# Install: pip install python-dotenv
try:
    from dotenv import load_dotenv
    _env_path = BASE_DIR / '.env'
    load_dotenv(_env_path, override=False)   # override=False: real env vars take priority
except ImportError:
    pass  # No dotenv — rely on system environment variables

SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production-please')
DEBUG = os.environ.get('DEBUG', 'True') == 'True'

# ── ALLOWED_HOSTS ──────────────────────────────────────────────────────
# Splits comma-separated env var. Also auto-detects GitHub Codespaces host.
_raw_hosts = os.environ.get('ALLOWED_HOSTS', 'localhost,127.0.0.1')
ALLOWED_HOSTS = [h.strip() for h in _raw_hosts.split(',') if h.strip()]

# GitHub Codespaces: CODESPACE_NAME is set automatically
_codespace = os.environ.get('CODESPACE_NAME', '')
_github_host = os.environ.get('GITHUB_CODESPACES_PORT_FORWARDING_DOMAIN', 'app.github.dev')
if _codespace:
    ALLOWED_HOSTS += [
        f'{_codespace}-8000.{_github_host}',
        f'*.{_github_host}',
        'localhost',
        '127.0.0.1',
    ]

# Always allow wildcard in DEBUG mode so local dev never breaks
if DEBUG:
    ALLOWED_HOSTS.append('*')

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'rest_framework',
    'corsheaders',
    'accounts',
    'businesses',
    'reviews',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [{
    'BACKEND': 'django.template.backends.django.DjangoTemplates',
    'DIRS': [BASE_DIR / 'templates'],
    'APP_DIRS': True,
    'OPTIONS': {'context_processors': [
        'django.template.context_processors.debug',
        'django.template.context_processors.request',
        'django.contrib.auth.context_processors.auth',
        'django.contrib.messages.context_processors.messages',
        'reviews.context_processors.dashboard_context',
    ]},
}]

WSGI_APPLICATION = 'config.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

AUTH_USER_MODEL = 'accounts.User'
LOGIN_URL = '/accounts/login/'
LOGIN_REDIRECT_URL = '/dashboard/'
LOGOUT_REDIRECT_URL = '/'

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
     'OPTIONS': {'min_length': 8}},
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Kolkata'
USE_I18N = True
USE_TZ = True

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'static']
# Use manifest storage in production only — avoids 500 error when staticfiles/ doesn't exist
if DEBUG:
    STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'
else:
    STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ── CORS ───────────────────────────────────────────────────────────────
CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True

# ── CSRF ───────────────────────────────────────────────────────────────
# Trust the Codespaces forwarding domain so CSRF tokens work in the browser
CSRF_TRUSTED_ORIGINS = []
_app_url = os.environ.get('APP_URL', '')
if _app_url:
    CSRF_TRUSTED_ORIGINS.append(_app_url)
if _codespace:
    CSRF_TRUSTED_ORIGINS.append(f'https://{_codespace}-8000.{_github_host}')
    CSRF_TRUSTED_ORIGINS.append(f'https://*.{_github_host}')
# Always trust local origins
CSRF_TRUSTED_ORIGINS += ['http://localhost:8000', 'http://127.0.0.1:8000']

# ── SESSION / CSRF cookie settings ─────────────────────────────────────
# Codespaces serves over HTTPS — cookies must be SameSite=None for cross-origin
SESSION_COOKIE_SAMESITE = 'None' if not DEBUG else 'Lax'
SESSION_COOKIE_SECURE   = not DEBUG
CSRF_COOKIE_SAMESITE    = 'None' if not DEBUG else 'Lax'
CSRF_COOKIE_SECURE      = not DEBUG

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': ['rest_framework.permissions.IsAuthenticated'],
    'DEFAULT_AUTHENTICATION_CLASSES': ['rest_framework.authentication.SessionAuthentication'],
    'DEFAULT_RENDERER_CLASSES': ['rest_framework.renderers.JSONRenderer'],
}

# ── Email ──────────────────────────────────────────────────────────────
EMAIL_BACKEND = os.environ.get(
    'EMAIL_BACKEND', 'django.core.mail.backends.console.EmailBackend'
)
EMAIL_HOST          = os.environ.get('EMAIL_HOST', '')
EMAIL_PORT          = int(os.environ.get('EMAIL_PORT', 587))
EMAIL_USE_TLS       = True
EMAIL_HOST_USER     = os.environ.get('EMAIL_HOST_USER', '')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD', '')
DEFAULT_FROM_EMAIL  = os.environ.get('DEFAULT_FROM_EMAIL', 'ReviewPro <noreply@reviewpro.app>')

# ── Google Business API ────────────────────────────────────────────────
GOOGLE_CLIENT_ID     = os.environ.get('GOOGLE_CLIENT_ID', '')
GOOGLE_CLIENT_SECRET = os.environ.get('GOOGLE_CLIENT_SECRET', '')
GOOGLE_REDIRECT_URI  = os.environ.get(
    'GOOGLE_REDIRECT_URI', 'http://localhost:8000/api/auth/google/callback/'
)

# ── Anthropic AI ───────────────────────────────────────────────────────
ANTHROPIC_API_KEY = os.environ.get('ANTHROPIC_API_KEY', '')

# ── App ────────────────────────────────────────────────────────────────
APP_NAME = 'ReviewPro'
APP_URL  = os.environ.get('APP_URL', 'http://localhost:8000')