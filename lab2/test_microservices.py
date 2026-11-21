# test_microservices.py
import unittest
from fastapi.testclient import TestClient
from catalog_service import app as catalog_app
from lab3.preorder_service import app as preorder_app

class TestMicroservices(unittest.TestCase):

    def setUp(self):
        self.catalog_client = TestClient(catalog_app)
        self.preorder_client = TestClient(preorder_app)

    # --- Тести Каталогу ---
    def test_get_catalog_item_success(self):
        """Позитивний тест: Отримання товару з каталогу"""
        response = self.catalog_client.get("/items/1")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["name"], "iPhone 16 Pro")

    def test_get_catalog_item_not_found(self):
        """Негативний сценарій: Запит неіснуючого товару (HTTP 404)"""
        response = self.catalog_client.get("/items/999")
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json()["detail"], "Товар не знайдено в каталозі")

    # --- Тести Передзамовлень ---
    def test_create_preorder_success(self):
        """Позитивний тест: Створення передзамовлення"""
        payload = {"customer_name": "Іван", "item_id": 1, "quantity": 2}
        response = self.preorder_client.post("/preorders/", json=payload)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()["customer"], "Іван")

    def test_create_preorder_invalid_quantity(self):
        """Негативний сценарій: Спроба замовити некоректну кількість (HTTP 400)"""
        payload = {"customer_name": "Марія", "item_id": 1, "quantity": -3}
        response = self.preorder_client.post("/preorders/", json=payload)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["detail"], "Кількість товару повинна бути більше 0")

if __name__ == "__main__":
    unittest.main()