from preorder_manager import PreorderManager

def main():
    manager = PreorderManager()
    
    while True:
        print("\n--- Меню передзамовлень (Консольна версія) ---")
        print("1. Додати нове передзамовлення")
        print("2. Показати всі передзамовлення")
        print("3. Фільтрувати замовлення за категорією")
        print("4. Скасувати (видалити) передзамовлення")
        print("5. Розрахувати загальну вартість замовлень")
        print("6. Зберегти у файл та вийти")
        
        choice = input("Оберіть дію (1-6): ")
        
        if choice == '1':
            try:
                customer_name = input("Введіть ім'я замовника: ")
                category = input("Введіть категорію (Гаджети, Техніка, Одяг): ")
                item_name = input("Введіть назву товару: ")
                price = float(input("Введіть ціну товару: "))
                quantity = int(input("Введіть кількість (за замовчуванням 1): ") or 1)
                
                manager.add_preorder(customer_name, category, item_name, price, quantity)
                print("✅ Замовлення успішно додано!")
            except ValueError as e:
                print(f"❌ Помилка вводу: {e}")
                
        elif choice == '2':
            orders = manager.get_all_preorders()
            if not orders:
                print("Список порожній.")
            else:
                print("\nСписок замовлень:")
                for order in orders:
                    print(f"- [ID:{order['id']}] {order['customer']} замовив {order['item']} ({order['quantity']} шт.) на суму {order['total_price']}")
                
        elif choice == '3':
            category = input("Введіть категорію для фільтрації: ")
            filtered = manager.filter_by_category(category) 
            if not filtered:
                print("Замовлень не знайдено.")
            else:
                print(f"\nЗамовлення у категорії '{category}':")
                for order in filtered:
                    print(f"- [ID:{order['id']}] {order['customer']} - {order['item']}")
                    
        elif choice == '4':
            try:
                order_id = int(input("Введіть ID замовлення для скасування: "))
                manager.cancel_preorder(order_id)
                print("✅ Замовлення скасовано!")
            except (ValueError, KeyError) as e:
                print(f"❌ Помилка: {e}")
                
        elif choice == '5':
            total = manager.calculate_total_revenue()
            print(f"\n💰 Загальна вартість усіх передзамовлень: {total} грн")
            
        elif choice == '6':
            manager.save_to_file("preorders.json")
            print("Дані збережено. Роботу завершено.")
            break
        else:
            print("❌ Невірний вибір. Спробуйте ще раз.")

if __name__ == "__main__":
    main()