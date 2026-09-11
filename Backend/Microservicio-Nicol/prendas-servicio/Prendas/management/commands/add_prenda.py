from django.core.management.base import BaseCommand
from datetime import datetime, timezone
from Prendas.mongo import prendas_collection


class Command(BaseCommand):
    help = "Agrega una prenda a MongoDB desde la terminal"

    def add_arguments(self, parser):
        parser.add_argument("--nombre", required=True)
        parser.add_argument("--categoria", required=True)
        parser.add_argument("--cantidad", required=True, type=float)
        parser.add_argument("--descripcion", default="")
        parser.add_argument("--estado", default="disponible")

    def handle(self, *args, **options):
        documento = {
            "nombre": options["nombre"],
            "descripcion": options["descripcion"],
            "categoria": options["categoria"],
            "cantidad": options["cantidad"],
            "estado": options["estado"],
            "fechaCreacion": datetime.now(timezone.utc).isoformat(),
            "published_by": "manual-cli",
        }
        result = prendas_collection.insert_one(documento)
        self.stdout.write(self.style.SUCCESS(f"Prenda creada con id: {result.inserted_id}"))