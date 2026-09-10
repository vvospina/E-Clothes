from rest_framework import serializers  # Serializers de DRF para validar entrada/salida.


class MarketMaterialSerializer(serializers.Serializer):
    # No hereda de ModelSerializer porque no hay modelo Django detrás:
    # los datos viven en MongoDB, se validan a mano campo por campo.

    id = serializers.CharField(read_only=True)  # ObjectId de Mongo, ya convertido a string.

    name = serializers.CharField(max_length=150)  # Nombre del material.

    material_type = serializers.CharField(max_length=80)  # Categoría: tela, cuero, hilo...

    presentation = serializers.CharField(max_length=50)  # retazo, metro, rollo, kg, unidad.

    price = serializers.DecimalField(max_digits=12, decimal_places=2)  # Precio de esta presentación.

    currency = serializers.CharField(max_length=3, required=False, default="COP")  # Moneda.

    supplier = serializers.CharField(
        max_length=150, required=False, allow_blank=True, allow_null=True
    )  # Proveedor, opcional.

    description = serializers.CharField(
        required=False, allow_blank=True, allow_null=True
    )  # Descripción libre, opcional.

    active = serializers.BooleanField(required=False, default=True)  # Permite ocultar sin borrar.

    created_at = serializers.CharField(read_only=True)  # Fecha ISO de creación (string, como en companies).
    updated_at = serializers.CharField(read_only=True)  # Fecha ISO de última modificación.

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
