import django_filters  # Librería de filtros para DRF (django-filter).

from .models import MarketMaterial  # Modelo sobre el que se filtra.


class MarketMaterialFilter(django_filters.FilterSet):
    # Filtro exacto por tipo de material, ignorando mayúsculas/minúsculas.
    material_type = django_filters.CharFilter(field_name="material_type", lookup_expr="iexact")

    # Filtro exacto por presentación (retazo, metro, rollo, kg, unidad).
    presentation = django_filters.CharFilter(field_name="presentation", lookup_expr="iexact")

    # Búsqueda parcial por nombre.
    name = django_filters.CharFilter(field_name="name", lookup_expr="icontains")

    # Rango de precio: mínimo y máximo, ambos opcionales.
    price_min = django_filters.NumberFilter(field_name="price", lookup_expr="gte")
    price_max = django_filters.NumberFilter(field_name="price", lookup_expr="lte")

    # Permite filtrar solo materiales activos o inactivos.
    active = django_filters.BooleanFilter(field_name="active")

    class Meta:
        model = MarketMaterial
        fields = ["material_type", "presentation", "name", "price_min", "price_max", "active"]
