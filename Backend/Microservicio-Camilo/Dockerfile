# syntax=docker/dockerfile:1

# ============================================================
# IMAGEN DEL MICROSERVICIO
# ============================================================

FROM python:3.13-slim-bookworm

# Evita que Python genere archivos .pyc
# y permite ver los logs inmediatamente
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# La app "materials" vive dentro de materials_app/, no en la raíz.
# Esto hace que Python la encuentre igual que el truco de sys.path
# que se agregó en manage.py, pero aplicado también a gunicorn.
ENV PYTHONPATH=/app/materials_app

WORKDIR /app

# ============================================================
# DEPENDENCIAS DEL SISTEMA
# ============================================================

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        nginx \
    && rm -rf /var/lib/apt/lists/*

# ============================================================
# DEPENDENCIAS DE PYTHON
# ============================================================

COPY requirements.txt /tmp/requirements.txt

RUN python -m pip install \
    --no-cache-dir \
    -r /tmp/requirements.txt

# ============================================================
# CÓDIGO DEL MICROSERVICIO
# ============================================================

COPY . /app/

# ============================================================
# CONFIGURACIÓN DE NGINX
# ============================================================

COPY nginx.conf /etc/nginx/nginx.conf

# ============================================================
# SCRIPT DE INICIO
# ============================================================

COPY start.sh /start.sh

RUN sed -i 's/\r$//' /start.sh \
    && chmod +x /start.sh \
    && nginx -t

# ============================================================
# PUERTO
# ============================================================

EXPOSE 10000

# ============================================================
# INICIO DEL CONTENEDOR
# ============================================================

CMD ["/start.sh"]