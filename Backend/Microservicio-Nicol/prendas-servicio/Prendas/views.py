from datetime import datetime, timezone
from bson import ObjectId
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from Prendas.mongo import prendas_collection

REQUIRED_FIELDS = ["nombre", "categoria", "cantidad"]
ESTADOS_VALIDOS = {"disponible", "reservada", "agotada"}


def serialize_prenda(doc):
    return {
        "id": str(doc["_id"]),
        "nombre": doc.get("nombre"),
        "descripcion": doc.get("descripcion"),
        "categoria": doc.get("categoria"),
        "cantidad": doc.get("cantidad"),
        "estado": doc.get("estado"),
        "fechaCreacion": doc.get("fechaCreacion"),
    }


class PrendaViewSet(viewsets.ViewSet):

    def list(self, request):
        query = {}
        categoria = request.query_params.get("categoria")
        estado = request.query_params.get("estado")
        if categoria:
            query["categoria"] = categoria
        if estado:
            query["estado"] = estado
        prendas = list(prendas_collection.find(query))
        return Response([serialize_prenda(p) for p in prendas])

    def retrieve(self, request, pk=None):
        try:
            object_id = ObjectId(pk)
        except Exception:
            return Response({"detail": "id inválido"}, status=status.HTTP_400_BAD_REQUEST)
        prenda = prendas_collection.find_one({"_id": object_id})
        if not prenda:
            return Response({"detail": "Prenda no encontrada"}, status=status.HTTP_404_NOT_FOUND)
        return Response(serialize_prenda(prenda))

    def create(self, request):
        data = request.data
        missing = [f for f in REQUIRED_FIELDS if not data.get(f)]
        if missing:
            return Response({"detail": f"Faltan campos obligatorios: {', '.join(missing)}"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            cantidad = float(data.get("cantidad"))
        except (TypeError, ValueError):
            return Response({"detail": "cantidad debe ser numérica"}, status=status.HTTP_400_BAD_REQUEST)
        estado = data.get("estado", "disponible")
        if estado not in ESTADOS_VALIDOS:
            return Response({"detail": f"estado debe ser uno de: {', '.join(sorted(ESTADOS_VALIDOS))}"}, status=status.HTTP_400_BAD_REQUEST)
        firebase_user = getattr(request, "firebase_user", None)
        document = {
            "nombre": data.get("nombre"),
            "descripcion": data.get("descripcion", ""),
            "categoria": data.get("categoria"),
            "cantidad": cantidad,
            "estado": estado,
            "fechaCreacion": datetime.now(timezone.utc).isoformat(),
            "published_by": firebase_user.get("uid") if firebase_user else None,
        }
        result = prendas_collection.insert_one(document)
        document["_id"] = result.inserted_id
        return Response(serialize_prenda(document), status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):
        return self._update(request, pk, partial=False)

    def partial_update(self, request, pk=None):
        return self._update(request, pk, partial=True)

    def _update(self, request, pk, partial):
        try:
            object_id = ObjectId(pk)
        except Exception:
            return Response({"detail": "id inválido"}, status=status.HTTP_400_BAD_REQUEST)
        existing = prendas_collection.find_one({"_id": object_id})
        if not existing:
            return Response({"detail": "Prenda no encontrada"}, status=status.HTTP_404_NOT_FOUND)
        data = request.data
        if not partial:
            missing = [f for f in REQUIRED_FIELDS if not data.get(f)]
            if missing:
                return Response({"detail": f"Faltan campos obligatorios: {', '.join(missing)}"}, status=status.HTTP_400_BAD_REQUEST)
        updates = {}
        for field in ["nombre", "descripcion", "categoria"]:
            if field in data:
                updates[field] = data.get(field)
        if "cantidad" in data:
            try:
                updates["cantidad"] = float(data.get("cantidad"))
            except (TypeError, ValueError):
                return Response({"detail": "cantidad debe ser numérica"}, status=status.HTTP_400_BAD_REQUEST)
        if "estado" in data:
            estado = data.get("estado")
            if estado not in ESTADOS_VALIDOS:
                return Response({"detail": f"estado debe ser uno de: {', '.join(sorted(ESTADOS_VALIDOS))}"}, status=status.HTTP_400_BAD_REQUEST)
            updates["estado"] = estado
        if updates:
            prendas_collection.update_one({"_id": object_id}, {"$set": updates})
        updated = prendas_collection.find_one({"_id": object_id})
        return Response(serialize_prenda(updated))

    def destroy(self, request, pk=None):
        try:
            object_id = ObjectId(pk)
        except Exception:
            return Response({"detail": "id inválido"}, status=status.HTTP_400_BAD_REQUEST)
        result = prendas_collection.delete_one({"_id": object_id})
        if result.deleted_count == 0:
            return Response({"detail": "Prenda no encontrada"}, status=status.HTTP_404_NOT_FOUND)
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(["GET"])
@permission_classes([permissions.AllowAny])
def health(request):
    return Response({"status": "ok"})