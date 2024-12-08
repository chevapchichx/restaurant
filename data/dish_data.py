class Dish:
    def __init__(self, id_dish, dish_name, price, weight, menu_category):
        self.id_dish = int(id_dish)
        self.dish_name = str(dish_name)
        self.price = round(float(price), 2)
        self.weight = round(weight, 2)
        self.menu_category = menu_category
