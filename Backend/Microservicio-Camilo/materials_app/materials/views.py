from django_filters.rest_framework import DjangoFilterBackend  # Backend de filtros para las vistas.
from rest_framework import filters, generics, permissions  # Utilidades estándar de DRF.
from rest_framework.decorators import api_view, permission_classes  # Para vista de health estilo companies.
from rest_framework.response import Response  # Respuesta HTTP en formato DRF.

from .filters import MarketMaterialFilter  # Filtros de tipo/presentación/precio.
from .models import MarketMaterial  # Modelo del catálogo.
from .serializers import MarketMaterialSerializer  # Serializer del modelo.


class MarketMaterialListCreateView(generics.ListCreateAPIView):
    # GET: lista materiales (con filtros). POST: crea un material nuevo.
    queryset = MarketMaterial.objects.all()
    serializer_class = MarketMaterialSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = MarketMaterialFilter
    ordering_fields = ["price", "name", "material_type", "created_at"]
    ordering = ["material_type", "name"]
    # No se define permission_classes aquí a propósito: se hereda de
    # REST_FRAMEWORK["DEFAULT_PERMISSION_CLASSES"] en settings.py, para que
    # activar/desactivar la protección Firebase sea un cambio de un solo
    # lugar (settings) y no haya que tocar cada vista.


class MarketMaterialDetailView(generics.RetrieveUpdateDestroyAPIView):
    # GET/PUT/PATCH/DELETE sobre un material puntual.
    queryset = MarketMaterial.objects.all()
    serializer_class = MarketMaterialSerializer
    lookup_field = "pk"


@api_view(["GET"])
@permission_classes([permissions.AllowAny])
def health(request):
    # Endpoint mínimo para verificar que el backend está respondiendo,
    # igual patrón que companies.views.health.
    return Response({"status": "ok", "service": "market-materials"})
