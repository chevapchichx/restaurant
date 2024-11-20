import sys
import os
from PyQt6.QtWidgets import QMessageBox
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from service.user_service import *


def open_order_list_window(self):
    from view.order_list_window import Order_List_Window
    self.waiter_window = Order_List_Window()  
    self.waiter_window.show()
    self.hide()  

def get_auth(self):
    user_service = User_Service()
    login = self.login_input.text().strip()
    password = self.password_input.text().strip()
    result = user_service.fill_user(login, password)

    if result == "":
        user = user_service.authorised_user
        if user.role == User_Role.WAITER:
            open_order_list_window(self)
        elif user.role == User_Role.COOK:
            print(f"Повар: {user.first_name} {user.last_name}")
        elif user.role == User_Role.ADMIN:
            print(f"Администратор: {user.first_name} {user.last_name}")
    else:
        QMessageBox.critical(self, "Ошибка", result)