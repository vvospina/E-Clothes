"""Define las rutas y endpoints expuestos bajo el prefijo de la API v1."""

from django.urls import path
from .views import consejos_list_create, consejo_detail, health

urlpatterns = [
    # Endpoint para listar todos los consejos ambientales (GET) o crear uno nuevo (POST)
    path('consejos/', consejos_list_create, name='consejos-list-create'),
    
    # Endpoint para consultar el detalle de un consejo específico utilizando su identificador único (PK)
    path('consejos/<str:pk>/', consejo_detail, name='consejo-detail'),
    
    # Endpoint público de verificación de estado para supervisar la disponibilidad del microservicio
    path('health/', health, name='health'),
]