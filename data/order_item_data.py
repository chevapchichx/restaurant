from enum import IntEnum

class DishStatus(IntEnum):  
    CREATED = 1
    COOKING = 2
    COOKED = 3

class OrderItem:
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
    
    def __init__(self, id_order_item, dish, amount, status, id_order):
        self.id_order_item = int(id_order_item)
        self.dish = dish
        self.amount = int(amount)
        self.__status = status
        self.id_order = int(id_order)
        

    def __get_status_name(self): 
        if self.status == DishStatus.CREATED:
            return "Добавлено"
        if self.status == DishStatus.COOKING:
            return "Готовится"
        if self.status == DishStatus.COOKED:
            return "Приготовлено"