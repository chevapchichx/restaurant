from user_data import *
from enum import IntEnum

class Order_Status(IntEnum):
    CREATED = 1
    COOKING = 2
    COOKED = 3
    CLOSED = 4

class Order:
    __status = 0

    @property
    def status_name(self):
        return self.__get_status_name
    
    @property
    def status(self):
        return self.__status

    def __init__(self, worker, meal, table, order_date, order_time, status):
        self.worker = worker
        self.meal = list(meal)
        self.table = int(table)
        self.date = order_date
        self.time = order_time
        self.__status = int(status)

    def __get_status_name(self):
        if self.status == Order_Status.CREATED:
            return "Создан"
        if self.status == Order_Status.COOKING:
            return "Готовится"
        if self.status == Order_Status.COOKED:
            return "Приготовлен"
        if self.status == Order_Status.CLOSED:
            return "Закрыт"