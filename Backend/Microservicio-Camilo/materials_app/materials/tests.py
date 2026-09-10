from rest_framework import status  # Códigos HTTP legibles.
from rest_framework.test import APITestCase  # Caso de prueba con cliente API de DRF.

from .mongo import market_materials_collection  # Colección real de Mongo usada en las pruebas.


class MarketMaterialCRUDTests(APITestCase):
    # IMPORTANTE: como Mongo no tiene el rollback automático que sí tiene el
    # ORM de Django en las pruebas, limpiamos la colección a mano antes y
    # después de cada test para no dejar basura ni depender de datos previos.
    # Usa MONGO_DB_NAME de un entorno de pruebas/local, nunca el de producción.

    def setUp(self):
        market_materials_collection.delete_many({})
        result = market_materials_collection.insert_one({
            "name": "Tela de algodón",
            "material_type": "tela",
            "presentation": "retazo",
            "price": 6000.0,
            "currency": "COP",
            "supplier": None,
            "description": None,
            "active": True,
            "created_at": "2026-01-01T00:00:00+00:00",
            "updated_at": "2026-01-01T00:00:00+00:00",
        })
        self.material_id = str(result.inserted_id)
        self.list_url = "/api/v1/market-materials/"
        self.detail_url = f"/api/v1/market-materials/{self.material_id}/"

    def tearDown(self):
        market_materials_collection.delete_many({})

    # 1. Operación exitosa -------------------------------------------------
    def test_list_materials_success(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_material_success(self):
        payload = {
            "name": "Tela de lino",
            "material_type": "tela",
            "presentation": "metro",
            "price": "27000.00",
        }
        response = self.client.post(self.list_url, payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(market_materials_collection.count_documents({}), 2)

    def test_filter_by_type_and_presentation(self):
        market_materials_collection.insert_one({
            "name": "Cuero sintético", "material_type": "cuero", "presentation": "metro",
            "price": 35000.0, "currency": "COP", "active": True,
            "created_at": "2026-01-01T00:00:00+00:00", "updated_at": "2026-01-01T00:00:00+00:00",
        })
        response = self.client.get(self.list_url, {"material_type": "tela", "presentation": "retazo"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["name"], "Tela de algodón")

    # 2. Datos inválidos o incompletos --------------------------------------
    def test_create_material_missing_fields(self):
        response = self.client.post(self.list_url, {"name": "Sin tipo ni precio"})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_material_negative_price(self):
        payload = {
            "name": "Material inválido",
            "material_type": "tela",
            "presentation": "metro",
            "price": "-100.00",
        }
        response = self.client.post(self.list_url, payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # 3. Recurso inexistente --------------------------------------------------
    def test_get_nonexistent_material_returns_404(self):
        # ObjectId válido en formato, pero que no existe en la colección.
        response = self.client.get("/api/v1/market-materials/000000000000000000000000/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_malformed_id_returns_404(self):
        # Id que ni siquiera tiene formato de ObjectId válido.
        response = self.client.get("/api/v1/market-materials/no-es-un-objectid/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    # 4. Actualizar y eliminar -------------------------------------------------
    def test_update_material_price(self):
        response = self.client.patch(self.detail_url, {"price": "7000.00"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["price"], "7000.00")

    def test_delete_material(self):
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(market_materials_collection.count_documents({}), 0)

    # NOTA: cuando se active FirebaseAuthentication en settings.py, agregar
    # aquí un test que confirme 401/403 en POST/PUT/DELETE sin token válido.
