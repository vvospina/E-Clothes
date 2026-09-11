from django.core.management.base import BaseCommand
from datetime import datetime, timezone
from companies.mongo import material_listings_collection

from datetime import datetime, timezone
from django.core.management.base import BaseCommand
from companies.mongo import material_listings_collection

class Command(BaseCommand):
    help = "Crea datos demo de materiales en MongoDB"

    def handle(self, *args, **kwargs):
        # Verifica si ya existe un registro demo de material
        existing = material_listings_collection.find_one({"published_by": "demo-owner"})

        # Si no existe, crea los datos iniciales de prueba
        if not existing:
            material_listings_collection.insert_one({
                "material_type": "Algodón perchado",
                "quantity": 80,
                "unit": "metros",
                "color": "azul",
                "densidad": "pesado",
                "status": "available",
                "published_by": "demo-owner",
                "created_at": datetime.now(timezone.utc).isoformat(),
            })
            self.stdout.write(self.style.SUCCESS("Datos demo creados en MongoDB"))
        else:
            self.stdout.write(self.style.WARNING("Los datos demo ya existen en MongoDB"))