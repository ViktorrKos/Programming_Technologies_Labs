# test_preorder_manager.py
import json
import unittest
from unittest.mock import patch, mock_open

try:
    from lab3.preorder_manager import PreorderManager
except ModuleNotFoundError:
    from lab2.preorder_manager import PreorderManager


class TestPreorderManager(unittest.TestCase):

    def setUp(self):
        """Виконується перед кожним тестом"""
        self.manager = PreorderManager()
        # Початкове заповнення тестовими даними
        self.manager.add_preorder("Олексій", "Гаджети", "iPhone 16 Pro", 1200.0, 1)
        self.manager.add_preorder("Марія", "Одяг", "Куртка", 150.0, 2)

    def test_add_preorder_success(self):
        """Позитивний тест: Успішне додавання передзамовлення"""
        order = self.manager.add_preorder("Іван", "Техніка", "Телевізор", 800.0, 1)
        self.assertEqual(order["id"], 3)
        self.assertEqual(len(self.manager.get_all_preorders()), 3)

    def test_add_preorder_invalid_price_raises_exception(self):
        """Негативний сценарій: Спроба додати замовлення з від'ємною ціною (ValueError)"""
        with self.assertRaises(ValueError):
            self.manager.add_preorder("Олена", "Гаджети", "Планшет", -500.0, 1)

    def test_add_preorder_empty_name_raises_exception(self):
        """Негативний сценарій: Спроба додати замовлення з порожнім ім'ям (ValueError)"""
        with self.assertRaises(ValueError):
            self.manager.add_preorder("", "Гаджети", "Планшет", 500.0, 1)

    def test_filter_by_category(self):
        """Позитивний тест: Фільтрація за категорією"""
        gadgets = self.manager.filter_by_category("Гаджети")
        self.assertEqual(len(gadgets), 1)
        self.assertEqual(gadgets[0]["item"], "iPhone 16 Pro")

    def test_cancel_preorder_success(self):
        """Позитивний тест: Видалення передзамовлення"""
        result = self.manager.cancel_preorder(1)
        self.assertTrue(result)
        self.assertEqual(len(self.manager.get_all_preorders()), 1)

    def test_cancel_preorder_not_found_raises_exception(self):
        """Негативний сценарій: Видалення неіснуючого замовлення (KeyError)"""
        with self.assertRaises(KeyError):
            self.manager.cancel_preorder(999)

    def test_calculate_total_revenue(self):
        """Позитивний тест: Підрахунок загальної суми (1200 + 150*2 = 1500)"""
        total = self.manager.calculate_total_revenue()
        self.assertEqual(total, 1500.0)

    @unittest.expectedFailure
    def test_feature_discount_promo_code_not_implemented(self):
        """Демонстрація @expectedFailure: тест нової фічі (промокод зі знижкою 10%), яка ще не реалізована.
        Тест впаде (AttributeError або AssertionError), але unittest не зарахує це як провал прогону."""
        # У PreorderManager ще немає методу apply_discount
        #self.manager.apply_discount("PROMO10")
        total = self.manager.calculate_total_revenue()
        self.assertEqual(total, 1500.0)

    # - Мок-тести для читання/запису файлів 

    def test_save_to_file_mock(self):
        """Тест збереження у файл за допомогою mock_open (ізоляція від файлової системи)"""
        fake_path = "fake/path/orders.json"
        target_open = f"{PreorderManager.__module__}.open"

        with patch(target_open, mock_open()) as mocked_file:
            self.manager.save_to_file(fake_path)
            # Перевіряємо, що файл було відкрито саме на запис
            mocked_file.assert_called_with(fake_path, "w", encoding="utf-8")

    def test_load_from_file_mock(self):
        """Тест зчитування з файлу за допомогою mock_open"""
        fake_path = "fake/path/orders.json"
        mock_data = json.dumps([
            {"id": 1, "customer": "Тестовий Клієнт", "category": "Книги", "item": "Python", "price": 50.0, "quantity": 1, "total_price": 50.0}
        ])
        target_open = f"{PreorderManager.__module__}.open"

        with patch(target_open, mock_open(read_data=mock_data)) as mocked_file:
            new_manager = PreorderManager()
            new_manager.load_from_file(fake_path)
            # Перевіряємо відкриття на читання
            mocked_file.assert_called_with(fake_path, "r", encoding="utf-8")
            self.assertEqual(len(new_manager.get_all_preorders()), 1)
            self.assertEqual(new_manager.get_all_preorders()[0]["customer"], "Тестовий Клієнт")


if __name__ == '__main__':
    unittest.main()
