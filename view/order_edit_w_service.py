import sys
import os
from service.order_service import *
from service.dish_service import DishService
from PyQt6.QtWidgets import QLabel, QPushButton, QSpinBox, QMessageBox
from data.order_item_data import DishStatus
from data.order_data import OrderStatus
from PyQt6.QtCore import Qt
from functools import partial

def open_order_list_window(self):
    from view.order_list_window import OrderListWindow
    self.waiter_window = OrderListWindow()
    self.waiter_window.ui_update_order_list_table()
    self.waiter_window.show()
    self.close()

def update_dish_sum(self):
    total_sum = 0
    for order_item in self.order.order_items:
        total_sum += order_item.dish_sum
    self.total_sum_label.setText(f"Итого: {total_sum} руб.")

def update_or_pay_order(self):
    if self.adding_dish_mode == True:
        update_order_items_and_order_status(self)
    else:
        update_order_status(self)

def update_order_item_amount(self):
    spinbox = self.sender()
    order_item = self.dish_spinboxes[spinbox]
    if spinbox.value() == 0:
        msg = QMessageBox.question(self, "Подтверждение", f"Удалить блюдо {order_item.dish.dish_name} из заказа?", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if msg == QMessageBox.StandardButton.Yes:
            OrderService().delete_order_item(order_item, self.order.id_order)
            self.order.order_items.remove(order_item)
            self.ui_update_dishes_layout()
            update_dish_sum(self)
        else:
            spinbox.setValue(order_item.amount)
            return
    order_item.amount = spinbox.value()
    OrderService().update_order_item_amount(order_item)
    update_dish_sum(self)

def delete_dish(self, order_item, id_order):
    msg = QMessageBox.question(self, "Подтверждение", f"Удалить блюдо {order_item.dish.dish_name} из заказа?", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
    if msg == QMessageBox.StandardButton.Yes:
        OrderService().delete_order_item(order_item, id_order)
        self.order.order_items.remove(order_item)
        self.ui_update_dishes_layout() 
    else:
        pass

def update_dishes_combobox(self):
    category_index = self.choose_category_combobox.currentIndex()
    category = self.categories[category_index - 1]
    self.choose_dish_combobox.clear()
    self.choose_dish_combobox.addItem("Не выбрано")
    if category_index > 0:
        self.dishes = DishService().get_dishes_by_category(category.id_menu_category)
        self.choose_dish_combobox.addItems([dish.dish_name for dish in self.dishes])
        self.choose_dish_combobox.setDisabled(False)

def add_dish_to_order(self):
    dish_index = self.choose_dish_combobox.currentIndex()
    dish = self.dishes[dish_index - 1]
    if dish_index == 0:
        return
    dish = DishService().get_dish_by_id(dish.id_dish)
    matching_item = next(
        (item for item in self.order.order_items 
         if item.dish.id_dish == dish.id_dish and item.status == DishStatus.CREATED), 
        None
    )
    if matching_item:
        matching_item.amount += 1
        OrderService().update_order_item_amount(matching_item)
        self.ui_update_dishes_layout()
        update_dish_sum(self)
        self.choose_dish_combobox.setCurrentIndex(0)
        return
    else:
        id_order_item = OrderService().add_dish_to_order(self.order.id_order, dish)
        order_item = OrderService().get_order_item_by_id(id_order_item)
        if order_item is not None:
            self.order.order_items.append(order_item)
            OrderService().update_order_status(self.order, OrderStatus.COOKING)
            self.ui_update_dishes_layout()
            update_dish_sum(self)
            self.choose_dish_combobox.setCurrentIndex(0)
            return

def update_order_items_and_order_status(self):
    if not self.order.order_items:
        QMessageBox.critical(self, "Ошибка", "Заказ пуст")
        return
    OrderService().update_order_items_status(self.order, DishStatus.COOKING)
    OrderService().update_order_status(self.order, OrderStatus.COOKING)
    open_order_list_window(self)

def update_order_status(self):
    self.update_or_pay_button.setText("Оплатить заказ")
    if OrderService().update_order_status(self.order, OrderStatus.CLOSED):
        open_order_list_window(self)
    else:
        QMessageBox.critical(self, "Ошибка", "Ошибка при закрытии заказа")