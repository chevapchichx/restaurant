from service.database_service import DatabaseService
from data.dish_data import Dish
from data.order_item_data import OrderItem
from data.menu_category_data import MenuCategory


class DishService:
    def get_menu_categories(self):
        data_service = DatabaseService()
        query = data_service.get_menu_categories_db()
        if query.error is None:
            result = query.result
            if result:
                categories = [MenuCategory(
                    id_menu_category=row[0],
                    name=row[1])
                    for row in result]
                return categories
            else:
                return "Категории не найдены"

        else:
            return f"Ошибка подключения к базе данных: {query.error}"

    
    def get_dishes_by_category(self, id_menu_category):
        data_service = DatabaseService()
        query = data_service.get_dishes_by_category_db(id_menu_category)
        if query.error is None:
            result = query.result
            if result:
                dishes = [Dish(
                    id_dish=row[0],
                    dish_name=row[1],
                    price=row[2],
                    weight=row[3],
                    menu_category=row[4])
                    for row in result]
                return dishes
            else:
                return "Блюда не найдены"
        else:
            return f"Ошибка подключения к базе данных: {query.error}"
    
    def get_dish_by_id(self, id_dish):    
        data_service = DatabaseService()
        query = data_service.get_dish_by_id_db(id_dish)
        if query.error is None:
            result = query.result
            if result:
                dish = Dish(
                    id_dish=result[0],
                    dish_name=result[1],
                    price=result[2],
                    weight=result[3],
                    menu_category=result[4])
                return dish
            else:
                return None
        else:
            return f"Ошибка подключения к базе данных: {query.error}"

