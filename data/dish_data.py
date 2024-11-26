from enum import IntEnum

class Dish_Status(IntEnum):
    CREATED = 1
    COOKING = 2
    COOKED = 3

class Dish:
    __status = 0

    @property
    def status_name(self):
        return self.__get_status_name()
    
    @property
    def status(self):
        return self.__status

    def __init__(self, id_dish, dish_name, price, weight, photo, menu_category, dish_status, amount):
        self.id_dish = int(id_dish)
        self.dish_name = str(dish_name)
        self.price = round(float(price), 2)
        self.weight = round(weight, 2)
        self.photo = str(photo)
        self.menu_category = menu_category
        self.__status = int(dish_status)
        self.amount = round(float(amount), 2)

    def __get_status_name(self):
        if self.status == Dish_Status.CREATED:
            return "Создан"
        if self.status == Dish_Status.COOKING:
            return "Готовится"
        if self.status == Dish_Status.COOKED:
            return "Приготовлен"
