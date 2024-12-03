from enum import IntEnum

class Order_Status(IntEnum):
    CREATED = 1
    COOKING = 2
    COOKED = 3
    CLOSED = 4

class Order:
    __status = 0

    @property
    def full_date(self):
        return f"{self.date} {self.time}"

    @property
    def status_name(self):
        return self.__get_status_name()
    
    @property
    def status(self):
        return self.__status

    def __init__(self, id_order, order_num, guests, worker, table, order_date, order_time, order_status, dishes, total_sum):
        self.id_order = int(id_order)
        self.order_num = int(order_num)
        self.guests = int(guests)
        self.worker = worker
        self.table = table
        self.date = order_date
        self.time = order_time
        self.__status = int(order_status)
        self.dishes = dishes
        self.total_sum = float(total_sum)

    def __get_status_name(self):
        if self.status == Order_Status.CREATED:
            return "Создан"
        if self.status == Order_Status.COOKING:
            return "Готовится"
        if self.status == Order_Status.COOKED:
            return "Приготовлен"
        if self.status == Order_Status.CLOSED:
            return "Закрыт"