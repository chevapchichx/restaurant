from enum import IntEnum

class OrderStatus(IntEnum):
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
    def order_sum(self):
        return sum([item.dish_sum for item in self.order_items])

    @property
    def status_name(self):
        return self.__get_status_name()
    
    @property
    def status(self):
        return self.__status

    def __init__(self, id_order, order_num, guests, staff, table, order_date, order_time, order_status, order_items):
        self.id_order = int(id_order)
        self.order_num = int(order_num)
        self.guests = int(guests)
        self.staff = staff
        self.table = table
        self.date = order_date
        self.time = order_time
        self.__status = int(order_status)
        self.order_items = order_items
                

    def __get_status_name(self): 
        if self.status == OrderStatus.CREATED:
            return "Создан"
        if self.status == OrderStatus.COOKING:
            return "Готовится"
        if self.status == OrderStatus.COOKED:
            return "Приготовлен"
        if self.status == OrderStatus.CLOSED:
            return "Закрыт"