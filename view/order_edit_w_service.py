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
    for dish in self.order.dishes:
        if dish.status == Dish_Status.CREATED:
            amount = self.dish_spinboxes[spinbox_index].value()
            total_sum += amount * dish.price
            spinbox_index += 1  
        else:
            total_sum += dish.amount * dish.price
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
    

def delete_dish(self, dish):
    msg = QMessageBox.question(self, "Подтверждение", f"Удалить блюдо {dish.dish_name}?", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
    if msg == QMessageBox.StandardButton.Yes:
        self.order.dishes.remove(dish)
        Order_Service().delete_dish(dish)
        self.update_dishes_layout() 
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





