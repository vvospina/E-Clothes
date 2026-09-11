from django.contrib import admin  # Panel de administración de Django.
from django.urls import path, include  # Utilidades de enrutamiento.

urlpatterns = [
    path("admin/", admin.site.urls),  # Panel de administración.
    path("api/v1/", include("materials.urls")),  # Rutas del microservicio de materiales.
]