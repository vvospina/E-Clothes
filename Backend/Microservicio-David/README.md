# Microservicio de Materiales - EcoRed // E-Clothes

Microservicio backend desarrollado con **Django REST Framework** y **MongoDB** para la gestión de publicaciones de materiales sobrantes a la venta dentro del sistema EcoRed. El proyecto implementa un modelo de seguridad basado en autenticación por tokens de **Firebase** y estructuración modular por componentes.

## Específicación del Documento / Modelo

Las publicaciones de materiales gestionadas en MongoDB contienen la siguiente estructura de campos:

- `material_type` *(string)*: Tipo de textil o material (ej. Poliéster, Algodón).
- `quantity` *(number)*: Cantidad disponible.
- `unit` *(string)*: Unidad de medida (ej. metros, kg).
- `color` *(string)*: Color del material.
- `densidad` *(string)*: Clasificación de densidad (ej. liviano, pesado).
- `location` *(string)*: Ubicación o ciudad del material.
- `status` *(string)*: Estado de la publicación (`available`, `sold`, etc.).
- `published_by` *(string)*: UID del usuario autenticado proveniente de Firebase.
- `created_at` *(ISO String)*: Fecha y hora de creación.
- `updated_at` *(ISO String)*: Fecha y hora de última modificación.

---

## Endpoints de la API (`/api/v1/materials/`)

Todas las peticiones a estos endpoints requieren la cabecera de autenticación con el Token de Firebase:
`Authorization: Bearer <FIREBASE_ID_TOKEN>`

1. GET -> /api/v1/materials/ -> HTTP/1.1 200 OK
2. POST -> /api/v1/materials/ -> HTTP/1.1 201 Created
3. PUT -> /api/v1/materials/<id>/ HTTP/1.1 200 OK
3. DELETE -> /api/v1/materials/<id>/ HTTP/1.1 204 NO CONTENT

## Requisitos Previos

- Python 3.10+
- Instancia activa de MongoDB (local o MongoDB Atlas)
- Archivo de credenciales de Firebase Admin SDK (`.json`) configurado en el proyecto


## Inicio Rápido

1. **Clonar el repositorio y crear el entorno virtual:**
   ```bash
   python -m venv venv
   # En Windows:
   venv\Scripts\activate
   # En Linux/Mac:
   source venv/bin/activate
