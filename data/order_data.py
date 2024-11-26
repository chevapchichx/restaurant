# from user_data import *
from enum import IntEnum
from data.user_data import User

class Order_Status(IntEnum):
    CREATED = 1
    COOKING = 2
    COOKED = 3
    CLOSED = 4

class Order:
    __status = 0

    @property
    def status_name(self):
        return self.__get_status_name()
    
    @property
    def status(self):
        return self.__status

    def __init__(self, id_order, order_num, worker, table, order_date, order_time, order_status, dishes):
        self.id_order = int(id_order)
        self.order_num = int(order_num)
        self.worker = worker
        self.table = int(table)
        self.date = order_date
        self.time = order_time
        self.__status = int(order_status)
        self.dishes = dishes


    def __get_status_name(self):
        if self.status == Order_Status.CREATED:
            return "Создан"
        if self.status == Order_Status.COOKING:
            return "Готовится"
        if self.status == Order_Status.COOKED:
            return "Приготовлен"
        if self.status == Order_Status.CLOSED:
            return "Закрыт"