from django.core.management.base import BaseCommand  # Clase base para comandos manage.py.

from materials.models import MarketMaterial  # Modelo a poblar.

# Lista de materiales de ejemplo para pruebas locales.
SAMPLE_MATERIALS = [
    {"name": "Tela de algodón", "material_type": "tela", "presentation": "retazo", "price": 6000, "supplier": "Textiles Bogotá"},
    {"name": "Tela de algodón", "material_type": "tela", "presentation": "metro", "price": 18000, "supplier": "Textiles Bogotá"},
    {"name": "Tela de lino", "material_type": "tela", "presentation": "retazo", "price": 9000, "supplier": "Lino Andino"},
    {"name": "Tela de lino", "material_type": "tela", "presentation": "metro", "price": 27000, "supplier": "Lino Andino"},
    {"name": "Cuero sintético", "material_type": "cuero", "presentation": "retazo", "price": 12000, "supplier": "Cueros del Sur"},
    {"name": "Cuero sintético", "material_type": "cuero", "presentation": "metro", "price": 35000, "supplier": "Cueros del Sur"},
    {"name": "Hilo poliéster", "material_type": "hilo", "presentation": "rollo", "price": 4500, "supplier": "Insumos EcoRed"},
    {"name": "Botón plástico", "material_type": "botón", "presentation": "unidad", "price": 150, "supplier": "Insumos EcoRed"},
    {"name": "Cierre metálico", "material_type": "cierre", "presentation": "unidad", "price": 1800, "supplier": "Insumos EcoRed"},
]


class Command(BaseCommand):
    help = "Carga materiales de mercado de ejemplo para pruebas locales."

    def handle(self, *args, **options):
        # Usa get_or_create para poder correr el comando varias veces sin duplicar filas.
        created = 0
        for item in SAMPLE_MATERIALS:
            _, was_created = MarketMaterial.objects.get_or_create(
                name=item["name"],
                material_type=item["material_type"],
                presentation=item["presentation"],
                defaults={
                    "price": item["price"],
                    "supplier": item.get("supplier", ""),
                },
            )
            created += int(was_created)

        self.stdout.write(self.style.SUCCESS(f"Listo. {created} materiales nuevos creados."))
