from PyQt6.QtWidgets import QMessageBox
import bcrypt
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from data.user_data import *
from service.database_service import *
from service.singleton import *

class User_Service(metaclass=SingletonMeta):
    __user: User = None

    @property
    def authorised_user(self):
        return self.__user
    
    def fill_user(self, login, password):
        data_service = Database_Service()
        query = data_service.get_user_db(login)
        if query.error is None:
            result = query.result   
            if result:
                hashed_password = result[10]
                if bcrypt.checkpw(password.encode('utf-8'), hashed_password):
                    self.__user = User(
                        role=result[0],
                        job=result[1], 
                        last_name=result[2], 
                        first_name=result[3], 
                        middle_name=result[4], 
                        birth_date=result[5], 
                        address=result[6], 
                        phone_number=result[7], 
                        salary=result[8], 
                        login=result[9], 
                        password=result[10])
                else:
                    return "Неверный пароль"
                if self.__user.role > len(User_Role) or self.__user.role < 1:
                    self.__user = None
                    return "Неизвестная роль пользователя"
                return ""
            else:
                return "Пользователь не найден"
        else:
            return f"Ошибка подключения к базе данных: {query.error}"

    
