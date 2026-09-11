from datetime import datetime, timezone  # Para timestamps de creación/actualización.

from bson import ObjectId  # Tipo de identificador nativo de MongoDB.
from bson.errors import InvalidId  # Error cuando un string no es un ObjectId válido.
from rest_framework import permissions, status  # Utilidades estándar de DRF.
from rest_framework.decorators import api_view, permission_classes  # Vista de health estilo companies.
from rest_framework.response import Response  # Respuesta HTTP en formato DRF.
from rest_framework.views import APIView  # Vista base para implementar el CRUD a mano.

from .mongo import market_materials_collection  # Colección de Mongo con los materiales.
from .serializers import MarketMaterialSerializer  # Validación de entrada/salida.


def _serialize(doc):
    # Convierte un documento de Mongo (dict con _id de tipo ObjectId) en un
    # dict listo para responder como JSON, con "id" como string.
    doc = dict(doc)
    doc["id"] = str(doc.pop("_id"))
    return doc


def _build_query(params):
    # Arma el filtro de Mongo a partir de los query params de la petición,
    # equivalente a lo que antes hacía django-filter con MySQL.
    query = {}

    material_type = params.get("material_type")
    if material_type:
        query["material_type"] = {"$regex": f"^{material_type}$", "$options": "i"}

    presentation = params.get("presentation")
    if presentation:
        query["presentation"] = {"$regex": f"^{presentation}$", "$options": "i"}

    name = params.get("name")
    if name:
        query["name"] = {"$regex": name, "$options": "i"}

    active = params.get("active")
    if active is not None:
        query["active"] = active.lower() == "true"

    price_min = params.get("price_min")
    price_max = params.get("price_max")
    if price_min or price_max:
        price_filter = {}
        if price_min:
            price_filter["$gte"] = float(price_min)
        if price_max:
            price_filter["$lte"] = float(price_max)
        query["price"] = price_filter

    return query


class MarketMaterialListCreateView(APIView):
    # GET: lista materiales (con filtros por query params). POST: crea uno nuevo.
    # No se define permission_classes aquí a propósito: se hereda de
    # REST_FRAMEWORK["DEFAULT_PERMISSION_CLASSES"] en settings.py.

    serializer_class = MarketMaterialSerializer  # Permite que la API navegable dibuje el formulario.

    def get_serializer(self, *args, **kwargs):
        # APIView no trae este método por defecto (a diferencia de los generics);
        # se agrega solo para que el renderer HTML sepa qué campos mostrar.
        return self.serializer_class(*args, **kwargs)

    def get(self, request):
        query = _build_query(request.query_params)
        cursor = market_materials_collection.find(query).sort(
            [("material_type", 1), ("name", 1)]
        )
        items = [_serialize(doc) for doc in cursor]
        return Response(items)

    def post(self, request):
        serializer = MarketMaterialSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)  # Lanza 400 automáticamente si falla.
        data = dict(serializer.validated_data)

        # Decimal no es serializable directo por pymongo/bson, se guarda como float.
        data["price"] = float(data["price"])
        data.setdefault("currency", "COP")
        data.setdefault("active", True)

        now = datetime.now(timezone.utc).isoformat()
        data["created_at"] = now
        data["updated_at"] = now

        result = market_materials_collection.insert_one(data)
        created = market_materials_collection.find_one({"_id": result.inserted_id})
        return Response(_serialize(created), status=status.HTTP_201_CREATED)


class MarketMaterialDetailView(APIView):
    # GET/PUT/PATCH/DELETE sobre un material puntual, identificado por su ObjectId.

    serializer_class = MarketMaterialSerializer  # Permite que la API navegable dibuje el formulario.

    def get_serializer(self, *args, **kwargs):
        return self.serializer_class(*args, **kwargs)

    def _get_object(self, pk):
        # Convierte el string de la URL a ObjectId; si no es válido, no existe.
        try:
            object_id = ObjectId(pk)
        except (InvalidId, TypeError):
            return None
        return market_materials_collection.find_one({"_id": object_id})

    def get(self, request, pk):
        doc = self._get_object(pk)
        if doc is None:
            return Response({"detail": "No encontrado."}, status=status.HTTP_404_NOT_FOUND)
        return Response(_serialize(doc))

    def put(self, request, pk):
        return self._update(request, pk, partial=False)

    def patch(self, request, pk):
        return self._update(request, pk, partial=True)

    def _update(self, request, pk, partial):
        doc = self._get_object(pk)
        if doc is None:
            return Response({"detail": "No encontrado."}, status=status.HTTP_404_NOT_FOUND)

        serializer = MarketMaterialSerializer(data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        updates = dict(serializer.validated_data)

        if "price" in updates:
            updates["price"] = float(updates["price"])
        updates["updated_at"] = datetime.now(timezone.utc).isoformat()

        market_materials_collection.update_one({"_id": doc["_id"]}, {"$set": updates})
        updated = market_materials_collection.find_one({"_id": doc["_id"]})
        return Response(_serialize(updated))

    def delete(self, request, pk):
        doc = self._get_object(pk)
        if doc is None:
            return Response({"detail": "No encontrado."}, status=status.HTTP_404_NOT_FOUND)
        market_materials_collection.delete_one({"_id": doc["_id"]})
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(["GET"])
@permission_classes([permissions.AllowAny])
def health(request):
    # Endpoint mínimo para verificar que el backend está respondiendo,
    # igual patrón que companies.views.health.
    return Response({"status": "ok", "service": "market-materials"})