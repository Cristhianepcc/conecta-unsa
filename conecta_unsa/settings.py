"""
Django settings for conecta_unsa (CONECTA UNSA).

Configuración 12-factor: todo lo sensible o dependiente del entorno se lee de
variables de entorno (ver `.env.example`). Obedece specs/constitucion.md §2 y
specs/requisitos-no-funcionales.md.
"""

import os
from pathlib import Path

import dj_database_url
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent

# Carga .env local (en producción las vars vienen del entorno de Railway).
load_dotenv(BASE_DIR / ".env")


def env_bool(name: str, default: bool = False) -> bool:
    return os.environ.get(name, str(default)).lower() in {"1", "true", "yes", "on"}


def env_list(name: str, default: str = "") -> list[str]:
    raw = os.environ.get(name, default)
    return [item.strip() for item in raw.split(",") if item.strip()]


# --- Seguridad / entorno (NFR-SEC-2/3) -------------------------------------
SECRET_KEY = os.environ.get(
    "SECRET_KEY",
    "django-insecure-dev-only-change-me-in-prod",
)

DEBUG = env_bool("DEBUG", True)

ALLOWED_HOSTS = env_list("ALLOWED_HOSTS", "localhost,127.0.0.1,.railway.app")

CSRF_TRUSTED_ORIGINS = env_list(
    "CSRF_TRUSTED_ORIGINS",
    "http://localhost:8000,http://127.0.0.1:8000,https://*.railway.app",
)


# --- Aplicaciones ----------------------------------------------------------
DJANGO_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",
]

# django-allauth preinstalado; los proveedores se configuran en la feature 02.
THIRD_PARTY_APPS = [
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "allauth.socialaccount.providers.google",
]

LOCAL_APPS = [
    "apps.core",
    "apps.taxonomia",
    "apps.usuarios",
    "apps.empresas",
    "apps.convocatorias",
    "apps.matching",
    "apps.notificaciones",
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "allauth.account.middleware.AccountMiddleware",
]

ROOT_URLCONF = "conecta_unsa.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "conecta_unsa.wsgi.application"


# --- Base de datos (CA-2): DATABASE_URL con fallback local ------------------
DATABASES = {
    "default": dj_database_url.config(
        default=os.environ.get(
            "DATABASE_URL",
            "postgres://project@localhost:5432/conecta_unsa",
        ),
        conn_max_age=600,
        conn_health_checks=True,
    )
}


# --- Autenticación ----------------------------------------------------------
AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
]

SITE_ID = 1

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]


# --- Internacionalización (CA-4 / NFR-I18N-1) -------------------------------
LANGUAGE_CODE = "es"
TIME_ZONE = "America/Lima"
USE_I18N = True
USE_TZ = True

# Moneda del dominio (PEN). Se usa en formato de plantillas.
CURRENCY_CODE = "PEN"
CURRENCY_SYMBOL = "S/"


# --- Estáticos (CA-3): WhiteNoise ------------------------------------------
STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = [BASE_DIR / "static"] if (BASE_DIR / "static").exists() else []

STORAGES = {
    "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}


# --- Endurecimiento producción (NFR-SEC-3): solo con DEBUG=False -------------
if not DEBUG:
    SECURE_SSL_REDIRECT = True
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    SECURE_CONTENT_TYPE_NOSNIFF = True


# --- Correo (Resend; se usa en feature 08) ---------------------------------
RESEND_API_KEY = os.environ.get("RESEND_API_KEY", "")
DEFAULT_FROM_EMAIL = os.environ.get(
    "DEFAULT_FROM_EMAIL", "CONECTA UNSA <no-reply@conecta-unsa.pe>"
)


DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
