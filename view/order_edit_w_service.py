import sys
import os
from service.order_service import *
from service.dish_service import Dish_Service
from PyQt6.QtWidgets import QLabel, QPushButton, QSpinBox, QMessageBox
from PyQt6.QtCore import Qt
from functools import partial

def open_order_list_window(self):
    from view.order_list_window import Order_List_Window
    self.waiter_window = Order_List_Window()
    self.close()
    # self.waiter_window.show()

def update_total_sum(self):
    total_sum = 0
    spinbox_index = 0  
    for order_item in self.order.order_items:
        # if dish.status == Dish_Status.CREATED:
        #     amount = self.dish_spinboxes[spinbox_index].value()
        #     total_sum += amount * dish.price
        #     spinbox_index += 1  
        # else:
        total_sum += order_item.dish_sum
    self.total_sum_label.setText(f"Сумма: {total_sum} руб.")

def save_order(self):
    total_sum = 0
    spinbox_index = 0  
    for dish in self.order.dishes:
        if dish.status == Dish_Status.CREATED:
            dish.amount = self.dish_spinboxes[spinbox_index].value()
            spinbox_index += 1  
        total_sum += dish.amount * dish.price
    self.order.total_sum = total_sum
    Order_Service().update_dish_amount(self.order)
    self.close()

    

def delete_dish(self, dish, id_order):
    msg = QMessageBox.question(self, "Подтверждение", f"Удалить блюдо {dish.dish_name}?", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
    if msg == QMessageBox.StandardButton.Yes:
        Order_Service().delete_dish(dish, id_order)
        self.order.dishes.remove(dish)
        self.ui_update_dishes_layout() 
    else:
        pass

def update_dishes_combobox(self):
    category = self.choose_category_combobox.currentText()
    if category == "Не выбрано":
        self.choose_dish_combobox.clear()
        self.choose_dish_combobox.addItem("Не выбрано")
    else:
        dishes = Dish_Service().get_dishes_by_category(category)
        self.choose_dish_combobox.clear()
        self.choose_dish_combobox.addItem("Не выбрано")
        self.choose_dish_combobox.addItems([dish.dish_name for dish in dishes])
        self.choose_dish_combobox.setDisabled(False)

def add_dish_to_order(self):
    dish_name = self.choose_dish_combobox.currentText()
    if dish_name == "Не выбрано":
        return
    dish = Dish_Service().get_dish_by_name(dish_name)
    if dish:
        print(f"Adding dish: {dish.dish_name}, id_dish: {dish.id_dish}")  # Отладочное сообщение
        self.order.dishes.append(dish)
        Order_Service().add_dish_to_order(self.order.id_order, dish.id_dish)
        self.ui_update_dishes_layout()
        update_total_sum(self)
        self.choose_dish_combobox.setCurrentIndex(0)





