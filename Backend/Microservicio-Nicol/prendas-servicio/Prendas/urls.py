from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import PrendaViewSet, health

# Crea un router para registrar rutas REST automáticamente.
router = DefaultRouter()

# Registra las rutas del recurso "prendas" según el contrato /api/v1/prendas.
router.register(r"prendas", PrendaViewSet, basename="prendas")

# Expone las rutas públicas de la app.
urlpatterns = [
    path("health/", health),
    path("", include(router.urls)),
]