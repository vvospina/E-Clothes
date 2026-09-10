from rest_framework import serializers  # Serializers de DRF para convertir modelos <-> JSON.

from .models import MarketMaterial  # Modelo que se va a serializar.


class MarketMaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = MarketMaterial  # Modelo asociado a este serializer.
        fields = [
            "id",
            "name",
            "material_type",
            "presentation",
            "price",
            "currency",
            "supplier",
            "description",
            "active",
            "created_at",
            "updated_at",
        ]  # Campos expuestos por la API.
        read_only_fields = ["id", "created_at", "updated_at"]  # El cliente no puede escribir estos.

    def validate_price(self, value):
        # Rechaza precios negativos o en cero.
        if value <= 0:
            raise serializers.ValidationError("El precio debe ser mayor que 0.")
        return value

    def validate_name(self, value):
        # Evita nombres vacíos o solo con espacios.
        if not value.strip():
            raise serializers.ValidationError("El nombre no puede estar vacío.")
        return value.strip()
