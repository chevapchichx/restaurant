import bcrypt
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from data.user_data import *
from .database_service import *
from .singleton import *

class User_Service(metaclass=SingletonMeta):
    __user: User = None

    @property
    def authorised_user(self):
        return self.__user
    
    def get_user(self, login, password):
        data_service = Database_Service()
        query = data_service.get_user_db(login)
        if query.error is None:
            result = query.result   
            if result:
                hashed_password = result[11]
                if bcrypt.checkpw(password.encode('utf-8'), hashed_password):
                    self.__user = User(
                        id_worker=result[0],
                        role=result[1],
                        job=result[2],
                        last_name=result[3],
                        first_name=result[4],
                        middle_name=result[5],
                        birth_date=result[6],
                        address=result[7],
                        phone_number=result[8],
                        salary=result[9],
                        login=result[10],
                        password=result[11])
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

    
