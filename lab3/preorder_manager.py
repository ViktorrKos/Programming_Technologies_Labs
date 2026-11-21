# preorder_manager.py
import json

class PreorderManager:
    def __init__(self):
        # Список для збереження замовлень
        self.preorders = []
        self._next_id = 1

    def add_preorder(self, customer_name: str, category: str, item_name: str, price: float, quantity: int = 1):
        """Метод 1: Додавання нового передзамовлення"""
        # Перевірка на коректність вхідних даних (виключення для негативних сценаріїв)
        if not customer_name or not item_name or not category:
            raise ValueError("Ім'я клієнта, категорія та назва товару не можуть бути порожніми.")
        if price <= 0:
            raise ValueError("Ціна товару повинна бути більшою за 0.")
        if quantity <= 0:
            raise ValueError("Кількість товару повинна бути більшою за 0.")

        order = {
            "id": self._next_id,
            "customer": customer_name,
            "category": category, # наприклад: "Гаджети", "Одяг", "Техніка"
            "item": item_name,
            "price": price,
            "quantity": quantity,
            "total_price": price * quantity
        }
        self.preorders.append(order)
        self._next_id += 1
        return order

    def get_all_preorders(self):
        """Метод 2: Отримання всіх передзамовлень"""
        return self.preorders

    def filter_by_category(self, category: str):
        """Метод 3: Фільтрація передзамовлень за категорією"""
        return [order for order in self.preorders if order["category"].lower() == category.lower()]

    def cancel_preorder(self, order_id: int):
        """Метод 4: Скасування (видалення) передзамовлення за ID"""
        for order in self.preorders:
            if order["id"] == order_id:
                self.preorders.remove(order)
                return True
        # Генерація виключення, якщо замовлення не знайдено
        raise KeyError(f"Передзамовлення з ID {order_id} не знайдено.")

    def calculate_total_revenue(self):
        """Метод 5: Підрахунок загальної суми всіх передзамовлень"""
        return sum(order["total_price"] for order in self.preorders)

    def save_to_file(self, filename: str):
        """Метод 6: Збереження списку передзамовлень у файл (JSON)"""
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(self.preorders, f, ensure_ascii=False, indent=2)

    def load_from_file(self, filename: str):
        """Метод 7: Завантаження списку передзамовлень з файлу (JSON)"""
        with open(filename, "r", encoding="utf-8") as f:
            self.preorders = json.load(f)
            if self.preorders:
                self._next_id = max(order["id"] for order in self.preorders) + 1
            else:
                self._next_id = 1
