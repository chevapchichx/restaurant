from service.database_service import Database_Service
from data.dish_data import Dish

class Dish_Service():
    def get_menu_categories(self):
        data_service = Database_Service()
        query = data_service.get_menu_categories_db()
        if query.error is None:
            result = query.result
            if result:
                categories = [row[0] for row in result]
                return categories
            else:
                return "Категории не найдены"
        else:
            return f"Ошибка подключения к базе данных: {query.error}"
    
    def get_dishes_by_category(self, category):
        data_service = Database_Service()
        query = data_service.get_dishes_by_category_db(category)
        if query.error is None:
            result = query.result
            if result:
                dishes = [Dish(
                    id_dish=row[0],
                    dish_name=row[1],
                    price=row[2],
                    weight=row[3],
                    photo=row[4],
                    menu_category=row[5],
                    dish_status=0, amount=0, dish_sum=0)
                    for row in result]
                return dishes
            else:
                return "Блюда не найдены"
        else:
            return f"Ошибка подключения к базе данных: {query.error}"

#     def fill_meals_by_order(self, id_order):
#         data_service = Database_Service()
#         query = data_service.get_meals_from_order_db(id_order)
#         if query.error is None:
#             result = query.result
#             if result:
#                 meals = [Dish(
#                     id_dish=row[0],
#                     dish_name=row[1],
#                     price=row[2],
#                     weight=row[3],
#                     photo=row[4],
#                     menu_section=row[5])
#                     for row in result]
#                 return meals
#             else:
#                 return "Блюда не найдены"
#         else:
#             return f"Ошибка подключения к базе данных: {query.error}"
    
    # def get_meal_by_id(self, id_meal):
    #     data_service = Database_Service()
    #     query = data_service.get_meal_by_id_db(id_meal)
    #     if query.error is None:
    #         result = query.result
    #         if result:
    #             meal = Meal(
    #                 id_meal=result[0],
    #                 meal_name=result[1],
    #                 price=result[2],
    #                 weight=result[3],
    #                 photo=result[4],
    #                 id_menu_section=result[5])
    #             return meal
    #         else:
    #             return "Блюдо не найдено"
    #     else:
    #         return f"Ошибка подключения к базе данных: {query.error}"