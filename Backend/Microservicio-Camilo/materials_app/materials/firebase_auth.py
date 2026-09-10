import os  # Permite leer variables de entorno del sistema operativo.
import logging  # Permite emitir trazas hacia consola usando la configuración LOGGING de Django.
import firebase_admin  # SDK administrativo de Firebase para Python.
from firebase_admin import credentials, auth  # credentials carga la credencial; auth valida tokens.
from rest_framework.authentication import BaseAuthentication  # Clase base para autenticación personalizada en DRF.
from rest_framework import exceptions  # Excepciones estándar de autenticación de DRF.
from dotenv import load_dotenv  # Carga variables desde el archivo .env.
from pathlib import Path  # Manejo robusto de rutas del sistema de archivos.

# ---------------------------------------------------------------------------
# IMPORTANTE: este archivo es una copia exacta del patrón usado en
# companies/firebase_auth.py, adaptada a este microservicio. Está lista para
# usarse, pero NO debe importarse todavía en settings.py: al importarse,
# inicializa Firebase Admin inmediatamente y si FIREBASE_CREDENTIALS_PATH no
# apunta a un JSON válido, revienta el arranque del proyecto con RuntimeError.
#
# Cuando el equipo termine de crear el nuevo proyecto Firebase:
#   1. Coloca el JSON de credenciales en este repo (nunca en git) y apunta
#      FIREBASE_CREDENTIALS_PATH hacia él en el .env.
#   2. En settings.py agrega "materials.firebase_auth.FirebaseAuthentication"
#      a DEFAULT_AUTHENTICATION_CLASSES y cambia DEFAULT_PERMISSION_CLASSES a
#      ["rest_framework.permissions.IsAuthenticatedOrReadOnly"].
#   3. Listo: las vistas de materials/views.py no necesitan ningún cambio,
#      porque heredan los permisos desde settings.
# ---------------------------------------------------------------------------

logger = logging.getLogger(__name__)  # Crea un logger asociado a este módulo.

# Calcula la ruta base del backend a partir de la ubicación de este archivo.
BASE_DIR = Path(__file__).resolve().parent.parent

# Carga las variables definidas en el .env del repo para poder leerlas con os.getenv().
load_dotenv(BASE_DIR / ".env")

# Lee desde variables de entorno la ruta del archivo de credenciales de Firebase.
cred_path = os.getenv("FIREBASE_CREDENTIALS_PATH")

# Valida que la ruta exista en la configuración antes de intentar usarla.
if not cred_path:
    raise RuntimeError("FIREBASE_CREDENTIALS_PATH no está definido en el archivo .env")

# Inicializa Firebase una sola vez para evitar errores por reinicialización del SDK.
if not firebase_admin._apps:
    cred = credentials.Certificate(cred_path)  # Carga el archivo JSON de credenciales del proyecto Firebase.
    firebase_admin.initialize_app(cred)  # Inicializa el SDK administrativo con esa credencial.
    logger.info("Firebase Admin inicializado correctamente")  # Deja una traza útil en consola.


class FirebaseUser:
    # Representa un usuario autenticado mínimo compatible con IsAuthenticated de DRF.
    def __init__(self, uid, email=None):
        self.uid = uid  # Identificador único del usuario en Firebase.
        self.email = email  # Correo del usuario, si el token lo incluye.
        self.is_authenticated = True  # Marca el objeto como autenticado para DRF.

    def __str__(self):
        # Devuelve una representación legible del usuario para logs o depuración.
        return self.email or self.uid


class FirebaseAuthentication(BaseAuthentication):
    # Implementa autenticación personalizada para validar tokens Bearer emitidos por Firebase.
    def authenticate(self, request):
        # Obtiene la cabecera Authorization enviada por el frontend.
        auth_header = request.headers.get("Authorization")

        # Registra si la petición llegó o no con la cabecera esperada.
        logger.info(f"Authorization presente: {bool(auth_header)}")

        # Si no existe cabecera, no autentica la solicitud y deja que DRF resuelva el permiso.
        if not auth_header:
            return None

        # Verifica que la cabecera tenga el formato Bearer <token>.
        if not auth_header.startswith("Bearer "):
            logger.warning("Cabecera Authorization mal formada")
            raise exceptions.AuthenticationFailed("Token mal formado")

        # Extrae el token quitando el prefijo 'Bearer '.
        id_token = auth_header.split("Bearer ", 1)[1].strip()

        # Verifica que después de Bearer realmente exista un token.
        if not id_token:
            logger.warning("La cabecera Authorization no contiene token")
            raise exceptions.AuthenticationFailed("Token vacío")

        try:
            # Valida el token directamente contra Firebase.
            decoded_token = auth.verify_id_token(id_token)

            # Guarda el payload decodificado en request para usarlo luego en las vistas.
            request.firebase_user = decoded_token

            # Construye un usuario mínimo para que DRF considere autenticada la request.
            user = FirebaseUser(
                uid=decoded_token.get("uid"),
                email=decoded_token.get("email"),
            )

            # Deja una traza con el uid autenticado.
            logger.info(f"Token válido para uid: {user.uid}")

            # Retorna el usuario autenticado y el token asociado.
            return (user, id_token)

        except Exception as e:
            # Registra el error real en consola para depuración.
            logger.exception(f"Error validando token de Firebase: {e}")

            # Responde a DRF con error de autenticación.
            raise exceptions.AuthenticationFailed("Token inválido")
