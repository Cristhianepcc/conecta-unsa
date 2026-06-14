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

# Modo demo: habilita accesos directos a los dashboards en el login (sin Google),
# para que el jurado vea los flujos. ⚠️ NO usar en producción real (apagar con DEMO_MODE=False).
DEMO_MODE = env_bool("DEMO_MODE", DEBUG)

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
    "apps.integraciones",
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
                "apps.notificaciones.context_processors.notificaciones",
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

# Login / logout (puertas en la feature 02-autenticacion)
LOGIN_URL = "usuarios:login"
LOGIN_REDIRECT_URL = "usuarios:post_login"
LOGOUT_REDIRECT_URL = "core:home"

# allauth: el ruteo de rol lo decide el adapter (la pestaña NO otorga permisos).
ACCOUNT_ADAPTER = "apps.usuarios.adapters.CuentaAdapter"
SOCIALACCOUNT_ADAPTER = "apps.usuarios.adapters.AdaptadorSocial"

ACCOUNT_LOGIN_METHODS = {"email"}
ACCOUNT_SIGNUP_FIELDS = ["email*"]
ACCOUNT_EMAIL_VERIFICATION = "none"  # demo; en prod se valida vía Google Workspace
SOCIALACCOUNT_LOGIN_ON_GET = True
SOCIALACCOUNT_EMAIL_AUTHENTICATION = True
SOCIALACCOUNT_EMAIL_VERIFICATION = "none"

SOCIALACCOUNT_PROVIDERS = {
    "google": {
        "SCOPE": ["profile", "email"],
        "AUTH_PARAMS": {"access_type": "online"},
        # TODO producción: agregar "hd": "unsa.edu.pe" para restringir el dominio
        # a la comunidad UNSA (auth-roles.md §3). En demo se acepta cualquier Gmail (CA-7).
        "APP": {
            "client_id": os.environ.get("GOOGLE_CLIENT_ID", ""),
            "secret": os.environ.get("GOOGLE_CLIENT_SECRET", ""),
            "key": "",
        },
    }
}

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

# --- Media subida por usuarios (logos/banners de empresa) ------------------
# Persistencia en un volumen de Railway: define MEDIA_ROOT con la ruta montada
# (p. ej. /data/media) para que los archivos sobrevivan a los despliegues.
MEDIA_URL = "media/"
MEDIA_ROOT = os.environ.get("MEDIA_ROOT", str(BASE_DIR / "media"))

STORAGES = {
    "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
    "staticfiles": {
        # Comprimido sin manifiesto: `{% static %}` funciona sin requerir collectstatic
        # (no rompe los tests, que corren con DEBUG=False). WhiteNoise igual sirve comprimido.
        "BACKEND": "whitenoise.storage.CompressedStaticFilesStorage",
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
# En dev (sin RESEND_API_KEY) los correos —incluido el reset de empresa— van a consola.
# Con RESEND_API_KEY se envía vía SMTP de Resend (feature 08). Override explícito con EMAIL_BACKEND.
if "EMAIL_BACKEND" in os.environ:
    EMAIL_BACKEND = os.environ["EMAIL_BACKEND"]
elif RESEND_API_KEY:
    EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
    EMAIL_HOST = "smtp.resend.com"
    EMAIL_PORT = 587
    EMAIL_USE_TLS = True
    EMAIL_HOST_USER = "resend"
    EMAIL_HOST_PASSWORD = RESEND_API_KEY
else:
    EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"


DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
