from django.core.management.base import BaseCommand
from datetime import datetime, timezone
from consejos.mongo import consejos_collection

class Command(BaseCommand):
    help = "Crea datos demo de consejos ambientales y de moda sostenible en MongoDB"

    def handle(self, *args, **kwargs):
        # Limpia la colección existente para asegurar datos limpios y actualizados
        consejos_collection.delete_many({})

        consejos_demo = [
            {
                "titulo": "El poder del secado al aire libre",
                "contenido": "Evita usar la secadora eléctrica siempre que puedas. Tender tus prendas al sol y al viento no solo ahorra una cantidad masiva de energía, sino que protege las fibras elásticas y evita que la ropa se encoja o desgaste prematuramente.",
                "categoria": "Cuidado de prendas",
                "created_at": datetime.now(timezone.utc).isoformat(),
            },
            {
                "titulo": "Transforma tus jeans en una bolsa reutilizable",
                "contenido": "¡No deseches esos viejos vaqueros rotos! Con un poco de costura básica puedes cortar las piernas y transformar la parte superior en una bolsa ecológica resistente para hacer mercado y reducir el uso de plásticos de un solo uso.",
                "categoria": "Reutilización",
                "created_at": datetime.now(timezone.utc).isoformat(),
            },
            {
                "titulo": "Repara antes de descartar (Visible Mending)",
                "contenido": "Un botón flojo o un pequeño desgarro no significan el fin de una prenda. Aplica técnicas de reparación creativa o bordado visible para darle una segunda vida única a tu ropa mientras adoptas un estilo de moda 100% circular.",
                "categoria": "Reciclaje textil",
                "created_at": datetime.now(timezone.utc).isoformat(),
            },
            {
                "titulo": "Lavados en frío para cuidar los tejidos",
                "contenido": "Cerca del 90% de la energía que usan las lavadoras se destina a calentar el agua. Lavar tu ropa con agua fría mantiene los colores vivos por más tiempo, cuida las telas sintéticas y reduce significativamente la huella de carbono de tu hogar.",
                "categoria": "Cuidado de prendas",
                "created_at": datetime.now(timezone.utc).isoformat(),
            }
        ]

        consejos_collection.insert_many(consejos_demo)
        
        # Muestra el mensaje de éxito usando el estilo de consola de Django
        self.stdout.write(
            self.style.SUCCESS("¡Consejos ambientales sostenibles sembrados con éxito en MongoDB!")
        )