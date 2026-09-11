from datetime import datetime, timezone  # Timestamps de creación.

from django.core.management.base import BaseCommand  # Clase base para comandos manage.py.

from materials.mongo import market_materials_collection  # Colección Mongo a poblar.

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
    help = "Carga materiales de mercado de ejemplo en MongoDB para pruebas locales."

    def handle(self, *args, **options):
        created = 0
        now = datetime.now(timezone.utc).isoformat()

        for item in SAMPLE_MATERIALS:
            # find_one_and_update con upsert: evita duplicar si se corre varias veces.
            existing = market_materials_collection.find_one({
                "name": item["name"],
                "material_type": item["material_type"],
                "presentation": item["presentation"],
            })
            if existing:
                continue

            market_materials_collection.insert_one({
                **item,
                "currency": "COP",
                "description": None,
                "active": True,
                "created_at": now,
                "updated_at": now,
            })
            created += 1

        self.stdout.write(self.style.SUCCESS(f"Listo. {created} materiales nuevos creados."))