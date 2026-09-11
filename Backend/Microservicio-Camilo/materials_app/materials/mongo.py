import os  # Permite leer variables de entorno del sistema operativo.
from pathlib import Path  # Manejo robusto de rutas del sistema de archivos.

from dotenv import load_dotenv  # Carga variables desde el archivo .env.
from pymongo import MongoClient  # Cliente de MongoDB.

# Calcula la ruta base del backend a partir de la ubicación de este archivo.
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Carga las variables definidas en el .env del repo.
load_dotenv(BASE_DIR / ".env")

# Lee la cadena de conexión y el nombre de la base de datos desde el .env.
MONGO_URI = os.getenv("MONGO_URI")
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME", "market_materials")

# Valida que la conexión esté configurada antes de intentar usarla.
if not MONGO_URI:
    raise RuntimeError("MONGO_URI no está definido en el archivo .env")

# Crea el cliente de Mongo una sola vez, al importar este módulo.
client = MongoClient(MONGO_URI)

# Selecciona la base de datos de este microservicio.
db = client[MONGO_DB_NAME]

# Colección donde se guardan los materiales del mercado.
market_materials_collection = db["market_materials"]