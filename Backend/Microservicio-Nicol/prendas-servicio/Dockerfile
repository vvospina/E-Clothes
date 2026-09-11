# syntax=docker/dockerfile:1

# ============================================================
# ETAPA 1 - Imagen Final de Django + Gunicorn
# ============================================================

FROM python:3.13-slim-bookworm

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Copiar archivo de requerimientos e instalar dependencias de Python
COPY requirements.txt /tmp/requirements.txt

RUN python -m pip install \
    --no-cache-dir \
    --upgrade pip \
    && python -m pip install \
    --no-cache-dir \
    -r /tmp/requirements.txt \
    gunicorn

# Copiar la totalidad del código del microservicio
COPY . /app/

# Exponer el puerto por defecto de producción
EXPOSE 8000

# Healthcheck apuntando al microservicio
HEALTHCHECK \
    --interval=30s \
    --timeout=5s \
    --start-period=10s \
    --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/', timeout=3)"

# Comando de inicio del WSGI de prendas-servicio mediante Gunicorn
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000"]