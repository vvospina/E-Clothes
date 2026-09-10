from datetime import datetime, timezone
from bson import ObjectId
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from companies.mongo import material_listings_collection

class MaterialListingViewSet(viewsets.ViewSet):
    # Exige autenticación para acceder a este conjunto de endpoints.
    permission_classes = [permissions.IsAuthenticated]

    # MÉTODOS PARA LISTAR MATERIALES
    def list(self, request):
        # Obtiene el uid del usuario autenticado desde Firebase.
        uid = request.firebase_user.get("uid")

        # Consulta directamente los materiales publicados por el usuario.
        items = list(material_listings_collection.find({"published_by": uid}))

        # Convierte identificadores a string para responder en JSON.
        for item in items:
            item["id"] = str(item["_id"])
            del item["_id"]

        # Retorna la lista de publicaciones.
        return Response(items)

    # MÉTODO CREATE DE MATERIALES
    def create(self, request):
        # Obtiene los datos enviados por el cliente.
        data = request.data

        # Construye el documento de publicación sin company_id.
        document = {
            "material_type": data.get("material_type"),
            "quantity": float(data.get("quantity")),
            "unit": data.get("unit", "metros"),
            "color": data.get("color"),
            "densidad": data.get("densidad"),
            "status": data.get("status", "available"),
            "published_by": request.firebase_user.get("uid"),
            "created_at": datetime.now(timezone.utc).isoformat(),
        }

        # Inserta la publicación en la colección.
        result = material_listings_collection.insert_one(document)

        # Retorna el id del documento creado.
        return Response({"id": str(result.inserted_id)}, status=status.HTTP_201_CREATED)

    # MÉTODO ELIMINAR MATERIALES
    def destroy(self, request, pk=None):
        uid = request.firebase_user.get("uid")

        try:
            item_id = ObjectId(pk)
        except Exception:
            return Response({"error": "ID inválido"}, status=status.HTTP_400_BAD_REQUEST)

        # Elimina si coincide el ID y fue publicada por este usuario.
        result = material_listings_collection.delete_one({
            "_id": item_id,
            "published_by": uid
        })

        if result.deleted_count == 0:
            return Response(
                {"error": "Publicación no encontrada o no tienes permisos para eliminarla"},
                status=status.HTTP_404_NOT_FOUND
            )

        return Response(status=status.HTTP_204_NO_CONTENT)

    # MÉTODO UPDATE DE MATERIALES
    def update(self, request, pk=None):
        """Actualización parcial o total de una publicación de material."""
        uid = request.firebase_user.get("uid")

        try:
            item_id = ObjectId(pk)
        except Exception:
            return Response({"error": "ID inválido"}, status=status.HTTP_400_BAD_REQUEST)

        data = request.data
        update_fields = {}

        # Construcción dinámica de los campos a actualizar
        if "material_type" in data:
            update_fields["material_type"] = data.get("material_type")

        if "quantity" in data:
            try:
                update_fields["quantity"] = float(data.get("quantity"))
            except (ValueError, TypeError):
                return Response(
                    {"error": "La cantidad debe ser un número válido"},
                    status=status.HTTP_400_BAD_REQUEST
                )

        if "unit" in data:
            update_fields["unit"] = data.get("unit")

        if "color" in data:
            update_fields["color"] = data.get("color")

        if "densidad" in data:
            update_fields["densidad"] = data.get("densidad")

        if "status" in data:
            update_fields["status"] = data.get("status")

        # Si no enviaron ningún campo válido para actualizar
        if not update_fields:
            return Response(
                {"error": "No se enviaron datos válidos para actualizar"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Agrega la fecha de última modificación
        update_fields["updated_at"] = datetime.now(timezone.utc).isoformat()

        # Actualiza el documento en MongoDB asegurando que pertenezca al usuario
        result = material_listings_collection.update_one(
            {"_id": item_id, "published_by": uid},
            {"$set": update_fields}
        )

        if result.matched_count == 0:
            return Response(
                {"error": "Publicación no encontrada o no tienes permisos para editarla"},
                status=status.HTTP_404_NOT_FOUND
            )

        return Response({"message": "Publicación actualizada correctamente"}, status=status.HTTP_200_OK)


@api_view(["GET"])
@permission_classes([permissions.AllowAny])
def health(request):
    # Endpoint mínimo para verificar que el backend está respondiendo.
    return Response({"status": "ok"})