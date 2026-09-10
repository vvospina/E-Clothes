from django.db import models  # Base de modelos de Django, usada para definir tablas en MySQL.


class MarketMaterial(models.Model):
    # Catálogo global de materiales del mercado. No depende de una empresa:
    # todos los usuarios consultan los mismos precios.
    #
    # Un mismo material (ej. 'Tela de algodón') puede tener varias filas,
    # una por cada presentación de venta (retazo, metro, rollo, kg...),
    # cada una con su propio precio.

    name = models.CharField(
        max_length=150,
        help_text="Nombre del material. Ej: 'Tela de algodón', 'Cuero sintético'.",
    )  # Nombre visible del material.

    material_type = models.CharField(
        max_length=80,
        db_index=True,
        help_text="Categoría del material. Ej: tela, cuero, hilo, botón, cierre.",
    )  # Categoría general, indexada porque se filtra seguido por este campo.

    presentation = models.CharField(
        max_length=50,
        db_index=True,
        help_text="Unidad/forma de venta. Ej: retazo, metro, rollo, kg, unidad.",
    )  # Forma en la que se vende ese material, también indexada para filtros.

    price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        help_text="Precio para esta presentación del material.",
    )  # Se usa Decimal (no float) para evitar errores de redondeo con dinero.

    currency = models.CharField(max_length=3, default="COP")  # Moneda del precio.

    supplier = models.CharField(max_length=150, blank=True, null=True)  # Proveedor opcional.

    description = models.TextField(blank=True, null=True)  # Descripción libre, opcional.

    active = models.BooleanField(default=True)  # Permite ocultar un material sin borrarlo.

    created_at = models.DateTimeField(auto_now_add=True)  # Fecha de creación automática.
    updated_at = models.DateTimeField(auto_now=True)  # Fecha de última modificación automática.

    class Meta:
        ordering = ["material_type", "name", "presentation"]  # Orden por defecto al listar.
        constraints = [
            # Evita duplicar el mismo material+presentación dos veces.
            models.UniqueConstraint(
                fields=["name", "material_type", "presentation"],
                name="unique_material_presentation",
            )
        ]

    def __str__(self):
        # Representación legible en el admin de Django y en logs.
        return f"{self.name} ({self.presentation}) - {self.price} {self.currency}"
