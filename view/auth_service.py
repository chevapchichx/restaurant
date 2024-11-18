import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from service.staff_service import *

def open_waiter_window(self, auth_info):
    from waiter_window import WaiterWindow
    self.waiter_window = WaiterWindow(auth_info)  
    self.waiter_window.show()
    self.hide()  

def open_auth_window(self):
    from auth_window import Auth_Window
    self.auth_window = Auth_Window()
    self.auth_window.show()
    self.close()  

def get_auth(self):
    login = self.login_input.text().strip()
    password = self.password_input.text().strip()
    auth_info = get_auth_waiter(login, password)

    if auth_info is not None:
        role = auth_info[2]
        if role == "Официант":
            open_waiter_window(self, auth_info)
        elif role == "Администратор":
            print(f"Администратор: {auth_info[3]} {auth_info[4]}")
        else:
            print("Неверный пароль")
    else:
        print("Неверные учетные данные")