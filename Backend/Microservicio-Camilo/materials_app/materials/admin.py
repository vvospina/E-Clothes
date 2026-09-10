from django.contrib import admin  # Panel de administración de Django.

from .models import MarketMaterial  # Modelo a registrar.


@admin.register(MarketMaterial)
class MarketMaterialAdmin(admin.ModelAdmin):
    list_display = ("name", "material_type", "presentation", "price", "currency", "active")
    list_filter = ("material_type", "presentation", "active")
    search_fields = ("name", "material_type", "supplier")
