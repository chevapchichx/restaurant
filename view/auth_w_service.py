import sys
import os
from PyQt6.QtWidgets import QMessageBox
from service.user_service import *
from view.order_list_window import OrderListWindow
from view.dish_list_window import DishListWindow

def open_order_list_window(self):
    self.waiter_window = OrderListWindow()  
    self.waiter_window.show()
    self.hide()  

def open_dish_list_window(self):
    self.cook_window = DishListWindow()
    self.cook_window.show()
    self.hide()

def get_auth(self):
    user_service = UserService()
    login = self.login_input.text().strip()
    password = self.password_input.text().strip()
    result = user_service.get_user(login, password)

    if result == "":
        user = user_service.authorised_user
        if user.role == UserRole.WAITER:
            open_order_list_window(self)
        elif user.role == UserRole.COOK:
            open_dish_list_window(self)
        elif user.role == UserRole.ADMIN:
            open_order_list_window(self)
    else:
        QMessageBox.critical(self, "Ошибка", result)