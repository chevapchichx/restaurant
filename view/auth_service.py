import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from service.staff_service import *

def get_auth(self):
    login = self.login_input.text().strip()
    password = self.password_input.text().strip()
    auth_info = get_auth_waiter(login, password)

    if auth_info is not None:
        role = auth_info[3]
        if role == "Официант":
            print(f"Официант: {auth_info[3]} {auth_info[4]}")
        elif role == "Администратор":
            print(f"Администратор: {auth_info[3]} {auth_info[4]}")
        else:
            print("Неверный пароль")
    else:
        print("Неверные учетные данные")