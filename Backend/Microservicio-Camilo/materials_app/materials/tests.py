from decimal import Decimal  # Para trabajar precios sin errores de redondeo.

from django.urls import reverse  # Resuelve URLs por nombre en vez de escribirlas a mano.
from rest_framework import status  # Códigos HTTP legibles.
from rest_framework.test import APITestCase  # Caso de prueba con cliente API de DRF.

from .models import MarketMaterial  # Modelo bajo prueba.


class MarketMaterialCRUDTests(APITestCase):
    def setUp(self):
        # Crea un material base antes de cada prueba.
        self.material = MarketMaterial.objects.create(
            name="Tela de algodón",
            material_type="tela",
            presentation="retazo",
            price=Decimal("6000.00"),
        )
        self.list_url = reverse("market-material-list")
        self.detail_url = reverse("market-material-detail", kwargs={"pk": self.material.pk})

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
        self.assertEqual(MarketMaterial.objects.count(), 2)

    def test_filter_by_type_and_presentation(self):
        MarketMaterial.objects.create(
            name="Cuero sintético", material_type="cuero", presentation="metro", price=Decimal("35000.00")
        )
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
        response = self.client.get(reverse("market-material-detail", kwargs={"pk": 9999}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    # 4. Actualizar y eliminar -------------------------------------------------
    def test_update_material_price(self):
        response = self.client.patch(self.detail_url, {"price": "7000.00"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.material.refresh_from_db()
        self.assertEqual(self.material.price, Decimal("7000.00"))

    def test_delete_material(self):
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(MarketMaterial.objects.filter(pk=self.material.pk).exists())

    # NOTA: cuando se active FirebaseAuthentication en settings.py, agregar
    # aquí un test que confirme 401/403 en POST/PUT/DELETE sin token válido,
    # igual al que exige el taller para los demás microservicios.
