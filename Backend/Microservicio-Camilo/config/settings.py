from pathlib import Path  # Manejo robusto de rutas del sistema de archivos.
from dotenv import load_dotenv  # Carga variables desde el archivo .env.
import os  # Permite leer variables de entorno del sistema operativo.

# Identifica la carpeta raíz del backend.
BASE_DIR = Path(__file__).resolve().parent.parent

# Carga las variables del archivo .env para que puedan leerse con os.getenv().
load_dotenv(BASE_DIR / ".env")

# Obtiene la clave secreta usada por Django desde variables de entorno.
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY")

# Convierte el valor de entorno en un booleano para activar o desactivar el modo debug.
DEBUG = os.getenv("DJANGO_DEBUG", "False") == "True"

# Convierte la lista de hosts permitidos en una lista Python separada por comas.
ALLOWED_HOSTS = os.getenv("DJANGO_ALLOWED_HOSTS", "127.0.0.1,localhost").split(",")

# Registra las aplicaciones instaladas en el proyecto.
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "corsheaders",
    "materials",
]

# Define la cadena de middlewares que procesa cada solicitud HTTP.
MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# TEMPLATES se mantiene aquí porque Django lo necesita para el panel admin,
# aunque el foco principal de este microservicio sea exponer una API REST.
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
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

# Indica a Django dónde está el archivo principal de rutas.
ROOT_URLCONF = "config.urls"

# Define el punto de entrada WSGI del proyecto.
WSGI_APPLICATION = "config.wsgi.application"

# Lee los orígenes permitidos para las peticiones del frontend.
CORS_ALLOWED_ORIGINS = os.getenv("CORS_ALLOWED_ORIGINS", "http://localhost:5173").split(",")

# ---------------------------------------------------------------------------
# Base de datos: los materiales viven en MongoDB (ver materials/mongo.py,
# conexión con pymongo, igual patrón que companies/mongo.py). Django igual
# necesita un DATABASES configurado para sus tablas internas (admin, auth,
# sesiones), así que se deja el sqlite por defecto — no se usa para los
# materiales, solo para lo interno de Django.
# ---------------------------------------------------------------------------
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# ---------------------------------------------------------------------------
# Django REST Framework.
#
# Autenticación Firebase ACTIVADA: las lecturas (GET) siguen siendo públicas,
# pero escribir (POST/PUT/PATCH/DELETE) exige un token válido en el header
# Authorization: Bearer <idToken>.
# ---------------------------------------------------------------------------
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "materials.firebase_auth.FirebaseAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
}

# Configuración general de idioma y zona horaria.
LANGUAGE_CODE = "es"
TIME_ZONE = "America/Bogota"
USE_I18N = True
USE_TZ = True

# Configuración de archivos estáticos.
STATIC_URL = "static/"

# Tipo de llave primaria por defecto para modelos Django.
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Configuración mínima de logs hacia consola.
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {"console": {"class": "logging.StreamHandler"}},
    "root": {"handlers": ["console"], "level": "INFO"},
}