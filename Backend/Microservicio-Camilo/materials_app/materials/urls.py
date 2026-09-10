from django.urls import path  # Utilidad para definir rutas.

from .views import MarketMaterialDetailView, MarketMaterialListCreateView, health  # Vistas de la app.

urlpatterns = [
    path("market-materials/", MarketMaterialListCreateView.as_view(), name="market-material-list"),
    # <str:pk> porque el id ahora es un ObjectId de Mongo (string), no un entero.
    path("market-materials/<str:pk>/", MarketMaterialDetailView.as_view(), name="market-material-detail"),
    path("health/", health, name="health-check"),
]
