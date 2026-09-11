from django.contrib import admin
from django.urls import path, include

# Define las rutas principales del proyecto.
urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/", include("Prendas.urls")),
]