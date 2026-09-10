# Microservicio: Materiales del Mercado

Estructura del repo (mismo patrón que tu backend actual: `manage.py` en la
raíz, carpeta `config/` con la configuración del proyecto, y la app como
carpeta hermana):

```
market-materials-service/
├── manage.py                 ← ya debe existir en tu repo (django-admin startproject)
├── config/
│   ├── __init__.py
│   ├── settings.py           ← REEMPLAZA por el que te entrego
│   ├── urls.py                ← REEMPLAZA por el que te entrego
│   ├── asgi.py                 ← ya debe existir, no se toca
│   └── wsgi.py                 ← ya debe existir, no se toca
├── materials/                  ← ESTA carpeta completa, pégala tal cual
│   ├── __init__.py
│   ├── apps.py
│   ├── models.py
│   ├── serializers.py
│   ├── filters.py
│   ├── views.py
│   ├── urls.py
│   ├── admin.py
│   ├── tests.py
│   ├── firebase_auth.py        ← listo, pero NO conectado todavía (ver abajo)
│   ├── migrations/
│   │   └── __init__.py
│   └── management/
│       ├── __init__.py
│       └── commands/
│           ├── __init__.py
│           └── seed_materials.py
├── .env                         ← lo creas tú a partir de .env.example, no se sube a git
├── .env.example                 ← REEMPLAZA/agrega el que te entrego
└── requirements.txt             ← REEMPLAZA/agrega el que te entrego
```

## Pasos para dejarlo corriendo

1. **Copiar `materials/`** completa a la raíz del repo, al lado de `config/`.
2. **Reemplazar `config/settings.py` y `config/urls.py`** por los que te entrego (ya incluyen todo lo de `materials`, MySQL y CORS).
3. **Instalar dependencias**:
   ```bash
   pip install -r requirements.txt
   ```
   (`mysqlclient` necesita las librerías de desarrollo de MySQL en el sistema; si falla la instalación, dímelo y te doy la alternativa con `pymysql`.)
4. **Crear el `.env`** a partir de `.env.example`, con tus credenciales de MySQL local. La línea de `FIREBASE_CREDENTIALS_PATH` queda **comentada** — no la actives todavía.
5. **Migrar y cargar datos de ejemplo**:
   ```bash
   python manage.py makemigrations materials
   python manage.py migrate
   python manage.py seed_materials
   python manage.py runserver
   ```
6. **Probar**: `GET http://localhost:8000/api/v1/market-materials/` ya debería devolver los 9 materiales de ejemplo, sin necesitar ningún token todavía.

## Endpoints

| Método | Ruta | Descripción |
|---|---|---|
| GET | `/api/v1/market-materials/` | Lista materiales. Filtros: `?material_type=tela&presentation=retazo&price_min=&price_max=&name=&active=` |
| POST | `/api/v1/market-materials/` | Crea un material |
| GET | `/api/v1/market-materials/{id}/` | Detalle |
| PUT/PATCH | `/api/v1/market-materials/{id}/` | Actualiza |
| DELETE | `/api/v1/market-materials/{id}/` | Elimina |
| GET | `/api/v1/health/` | Health check |

### Ejemplo para la ficha de contrato del equipo

**POST /api/v1/market-materials/**
```json
{
  "name": "Tela de algodón",
  "material_type": "tela",
  "presentation": "retazo",
  "price": "6000.00",
  "supplier": "Textiles Bogotá"
}
```

**201 Created**
```json
{
  "id": 1,
  "name": "Tela de algodón",
  "material_type": "tela",
  "presentation": "retazo",
  "price": "6000.00",
  "currency": "COP",
  "supplier": "Textiles Bogotá",
  "description": null,
  "active": true,
  "created_at": "2026-09-09T10:00:00Z",
  "updated_at": "2026-09-09T10:00:00Z"
}
```

**400 Bad Request** (precio inválido)
```json
{ "price": ["El precio debe ser mayor que 0."] }
```

## Correr las pruebas
```bash
python manage.py test materials
```

## Cuando el nuevo proyecto Firebase esté listo

`materials/firebase_auth.py` es una copia exacta del patrón de
`companies/firebase_auth.py`. Para activarlo:

1. Coloca el JSON de credenciales del **nuevo** proyecto Firebase en el repo (nunca en git) y en `.env` descomenta y ajusta:
   ```
   FIREBASE_CREDENTIALS_PATH=./firebase-service-account-materials.json
   ```
2. En `config/settings.py`, dentro de `REST_FRAMEWORK`, comenta la línea de `AllowAny` y descomenta el bloque de `DEFAULT_AUTHENTICATION_CLASSES` + `IsAuthenticatedOrReadOnly` que ya está escrito ahí mismo.
3. Reinicia el servidor.

No hace falta tocar `materials/views.py` ni `materials/urls.py`: los permisos se heredan desde `settings.py`, igual que en `companies`.
