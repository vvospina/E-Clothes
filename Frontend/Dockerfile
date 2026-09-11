# syntax=docker/dockerfile:1

# ------------------------------------------------------------------------
# Etapa 1: build de la SPA con Vite
# ------------------------------------------------------------------------
# Las variables VITE_* se "hornean" dentro del bundle en tiempo de build
# (Vite las reemplaza como texto plano), por eso se reciben como ARG/ENV
# aquí y NO como variables de entorno del contenedor final.
FROM node:20-alpine AS build
WORKDIR /app

COPY package*.json ./
RUN npm ci

COPY . .

ARG VITE_API_URL=/api/v1
ARG VITE_FIREBASE_API_KEY
ARG VITE_FIREBASE_AUTH_DOMAIN
ARG VITE_FIREBASE_PROJECT_ID
ARG VITE_FIREBASE_APP_ID
ARG VITE_MOCK_INSUMOS=true
ARG VITE_MOCK_MATERIALES_MERCADO=true
ARG VITE_MOCK_CONSEJOS=false
ARG VITE_MOCK_PRENDAS=true

ENV VITE_API_URL=$VITE_API_URL \
    VITE_FIREBASE_API_KEY=$VITE_FIREBASE_API_KEY \
    VITE_FIREBASE_AUTH_DOMAIN=$VITE_FIREBASE_AUTH_DOMAIN \
    VITE_FIREBASE_PROJECT_ID=$VITE_FIREBASE_PROJECT_ID \
    VITE_FIREBASE_APP_ID=$VITE_FIREBASE_APP_ID \
    VITE_MOCK_INSUMOS=$VITE_MOCK_INSUMOS \
    VITE_MOCK_MATERIALES_MERCADO=$VITE_MOCK_MATERIALES_MERCADO \
    VITE_MOCK_CONSEJOS=$VITE_MOCK_CONSEJOS \
    VITE_MOCK_PRENDAS=$VITE_MOCK_PRENDAS

RUN npm run build

# ------------------------------------------------------------------------
# Etapa 2: servir el build con Nginx (SPA + proxy hacia los microservicios)
# ------------------------------------------------------------------------
FROM nginx:1.27-alpine

# La plantilla se procesa automáticamente al arrancar el contenedor
# (envsubst sobre las variables INSUMOS_SERVICE_URL, MERCADO_SERVICE_URL,
# CONSEJOS_SERVICE_URL y PRENDAS_SERVICE_URL definidas en docker-compose).
COPY docker/nginx/default.conf.template /etc/nginx/templates/default.conf.template
COPY --from=build /app/dist /usr/share/nginx/html

EXPOSE 80

HEALTHCHECK --interval=30s --timeout=3s CMD wget -qO- http://localhost/ || exit 1
