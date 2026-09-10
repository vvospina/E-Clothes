import os
from pathlib import Path

from dotenv import load_dotenv
from pymongo import MongoClient


# Ruta raíz del microservicio:
# Microservicio-Camilo/
BASE_DIR = Path(__file__).resolve().parents[2]

# Carga el .env ubicado en:
# Microservicio-Camilo/.env
load_dotenv(BASE_DIR / ".env")


# Variables de MongoDB
MONGO_URI = os.getenv("MONGO_URI")
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME", "market_materials")


# Valida que la conexión esté configurada
if not MONGO_URI:
    raise RuntimeError(
        "MONGO_URI no está definido en el archivo .env"
    )


# Cliente de MongoDB
client = MongoClient(MONGO_URI)

# Base de datos
db = client[MONGO_DB_NAME]

# Colección de materiales
market_materials_collection = db["market_materials"]
