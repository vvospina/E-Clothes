# prendas-service

Microservicio de inventario de prendas para el proyecto EcoRed. Forma parte de la arquitectura de microservicios del equipo (ver `docker-compose.yaml` en la raíz del repositorio) y expone su API bajo la ruta pública `/api/v1/prendas`.

## Stack técnico

- **Framework:** Django 6 + Django REST Framework
- **Base de datos de negocio:** MongoDB (vía PyMongo), colección `prendas`
- **Autenticación:** Firebase Authentication (ID Token verificado con Firebase Admin SDK)
- **Base de datos interna:** SQLite (solo para apps propias de Django: `auth`, `admin`, `sessions`; los datos de negocio nunca pasan por aquí)
- **Servidor de producción:** Gunicorn
- **Contenerización:** Docker / Docker Compose

## Responsabilidad y datos propios

Este servicio gestiona el **inventario de prendas**: creación, consulta, edición y eliminación. No accede a datos internos de ningún otro microservicio del equipo; su única fuente de datos es su propia colección de MongoDB.

---

## Estructura del proyecto

```
backend-prendas/
├── Prendas/
│   ├── views.py            # Lógica de los endpoints (ViewSet + health check)
│   ├── urls.py              # Rutas del recurso "prendas"
│   ├── mongo.py             # Conexión a MongoDB
│   ├── firebase_auth.py     # Autenticación custom con Firebase ID Token
│   ├── tests.py             # Pruebas automatizadas (20 casos)
│   └── management/commands/ # Comandos de utilidad (seed de datos demo)
├── config/
│   ├── settings.py          # Configuración de Django/DRF/Mongo/CORS
│   ├── urls.py               # Punto de entrada de rutas (/api/v1/)
│   └── wsgi.py                # Entrypoint para Gunicorn
├── contracts/prendas-service/
│   ├── endpoints.md          # Ficha de contrato de cada endpoint
│   └── examples/*.json       # Ejemplos JSON de solicitud/respuesta (mocks)
├── Dockerfile
├── .dockerignore
├── docker-compose.yaml
├── .env.example
├── .gitignore
├── requirements.txt
└── manage.py
```

---

## Configuración local (sin Docker)

### 1. Requisitos

- Python 3.12+
- Una base de datos MongoDB accesible (Atlas o local)
- Un proyecto de Firebase con Authentication habilitado y un archivo de credenciales de servicio (JSON)

### 2. Variables de entorno

Copia `.env.example` a `.env` y completa los valores reales:

```bash
cp .env.example .env
```

| Variable | Descripción |
|---|---|
| `DJANGO_SECRET_KEY` | Clave secreta de Django (genera una propia, no la compartas) |
| `DJANGO_DEBUG` | `True` en desarrollo, `False` en producción |
| `DJANGO_ALLOWED_HOSTS` | Hosts permitidos, separados por coma |
| `PORT` | Puerto en el que corre el servidor (por defecto `8000`) |
| `MONGODB_URI` | Cadena de conexión a tu base MongoDB |
| `MONGODB_DB_NAME` | Nombre de la base de datos |
| `CORS_ALLOWED_ORIGINS` | Orígenes permitidos para CORS (el frontend, separados por coma) |
| `FIREBASE_CREDENTIALS_PATH` | Ruta al archivo JSON de credenciales de Firebase Admin |

**Nunca subas `.env` ni el archivo de credenciales de Firebase al repositorio.** Ambos están excluidos en `.gitignore` y `.dockerignore`.

### 3. Instalación y arranque

```bash
python -m venv venv
source venv/bin/activate          # En Windows: venv\Scripts\activate
pip install -r requirements.txt

python manage.py migrate --run-syncdb
python manage.py runserver
```

El servidor queda disponible en `http://127.0.0.1:8000`.

---

## Ejecución con Docker

```bash
docker compose config      # Valida la sintaxis del compose
docker compose build       # Construye la imagen
docker compose up -d       # Levanta el contenedor
docker compose ps          # Debe verse "healthy"
docker compose logs --tail=100 prendas-service
```

La imagen **no incluye** `.env` ni el archivo de credenciales de Firebase (ver `.dockerignore`); ambos se inyectan en tiempo de ejecución vía `env_file` y un volumen de solo lectura, según `docker-compose.yaml`.

---

## Contrato de la API

La ficha completa de cada endpoint —rutas, autenticación, atributos, tipos, obligatoriedad y ejemplos JSON de éxito/error— está en [`contracts/prendas-service/endpoints.md`](./contracts/prendas-service/endpoints.md). Los ejemplos JSON individuales (usables como mocks para el frontend) están en `contracts/prendas-service/examples/`.

### Resumen de endpoints

| Método | Ruta | Auth | Descripción |
|---|---|---|---|
| GET | `/api/v1/health/` | No | Estado del servicio |
| GET | `/api/v1/prendas/` | No | Listar prendas (filtros `?categoria=` y `?estado=`) |
| GET | `/api/v1/prendas/{id}/` | No | Consultar una prenda |
| POST | `/api/v1/prendas/` | Sí (Firebase) | Crear una prenda |
| PUT | `/api/v1/prendas/{id}/` | Sí (Firebase) | Reemplazar una prenda completa |
| PATCH | `/api/v1/prendas/{id}/` | Sí (Firebase) | Editar parcialmente una prenda |
| DELETE | `/api/v1/prendas/{id}/` | Sí (Firebase) | Eliminar una prenda |

Los endpoints protegidos requieren la cabecera:
```
Authorization: Bearer <ID_TOKEN_DE_FIREBASE>
```

---

## Pruebas automatizadas

```bash
python manage.py test Prendas -v 2
```

`Prendas/tests.py` cubre, para cada endpoint, los 5 casos mínimos exigidos por el taller:

1. Operación exitosa
2. Datos inválidos o incompletos
3. Token Firebase ausente o inválido
4. Recurso inexistente
5. Compatibilidad de la respuesta con la ficha de contrato

La colección de MongoDB y la verificación de Firebase se simulan con `unittest.mock`, por lo que las pruebas corren sin necesitar una base de datos real ni tokens de Firebase válidos.

---

## Notas de diseño y decisiones

- **Autenticación:** `FirebaseAuthentication` (en `Prendas/firebase_auth.py`) implementa `authenticate_header()` para que las peticiones sin token o con token inválido devuelvan `401 Unauthorized` en vez de `403 Forbidden` (comportamiento por defecto de DRF si no se declara ese método).
- **Lectura pública, escritura protegida:** se usa el permiso `IsAuthenticatedOrReadOnly` de DRF; cualquiera puede consultar el inventario, pero solo usuarios autenticados con Firebase pueden modificarlo.
- **Base de datos dual:** MongoDB para los datos de negocio (prendas) y SQLite solo para las apps internas de Django. Esto es intencional: el servicio no usa el ORM de Django para su dominio.

---

## Publicación en OCIR

_(Sección a completar en la Fase 4 del taller: ruta del repositorio OCIR, tag de versión y evidencia de verificación de la imagen publicada.)_