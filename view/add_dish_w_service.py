from PyQt6.QtWidgets import QMessageBox


def open_menu_management_window(self):
    from view.menu_management_window import MenuManagementWindow
    self.menu_window = MenuManagementWindow()
    self.menu_window.show()
    self.close()


def add_dish(self):
    dish_name = self.name_input.text().strip()

    try:
        price = float(self.price_input.text().strip())
        weight = float(self.weight_input.text().strip())
    except ValueError:
        self.error_label.setText("Ошибка в числовых значениях")
        return

    if price <= 0 or weight <= 0:
        self.error_label.setText(
            "Цена и вес должны быть положительными числами")
        return

    category_index = self.category_combo.currentIndex()
    if category_index < 0:
        self.error_label.setText("Выберите категорию")
        return

    category_id = self.categories[category_index].id_menu_category

    result = self.dish_service.add_dish(dish_name, price, weight, category_id)

    if result is True:
        open_menu_management_window(self)
    else:
        self.error_label.setText(f"Ошибка при добавлении блюда: {result}")
