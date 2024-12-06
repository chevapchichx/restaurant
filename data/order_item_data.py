from enum import IntEnum

class Dish_Status(IntEnum):
    CREATED = 1
    COOKING = 2
    COOKED = 3

class Order_Item:
    __status = 0

    @property
    def status_name(self):
        return self.__get_status_name()
    
    @property
    def status(self):
        return self.__status
    
    @property
    def dish_sum(self):
        return self.dish.price * self.amount
    
    def __init__(self, id_order_item, dish, amount, status):
        self.id_order_item = int(id_order_item)
        self.dish = dish
        self.amount = int(amount)
        self.__status = status
        

    def __get_status_name(self):
        if self.status == Dish_Status.CREATED:
            return "Добавлен"
        if self.status == Dish_Status.COOKING:
            return "Готовится"
        if self.status == Dish_Status.COOKED:
            return "Приготовлен"