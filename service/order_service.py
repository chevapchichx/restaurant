from data.order_data import *
from service.database_service import *
from service.singleton import *
from data.dish_data import *

class Order_Service:

    def get_orders(self, id_worker, role):
        data_service = Database_Service()
        query = data_service.get_orders_db(id_worker, role)
        if query.error is None:
            result = query.result   
            if result:
                orders = [Order(
                    id_order=row[0],
                    order_num=row[1],
                    worker=User(
                        id_worker=row[2],
                        role=row[3],
                        job=row[4],
                        last_name=row[5],
                        first_name=row[6],
                        middle_name=row[7],
                        birth_date=None, address=None, phone_number=None, salary=0, login=None, password=None),
                    table=row[8],
                    order_date=row[9],
                    order_time=row[10],
                    order_status=row[11],
                    dishes=[])
                    for row in result]
                return orders
            else:
                return "Заказы не найдены"
        else:
            return f"Ошибка подключения к базе данных: {query.error}"

    def get_order_for_edit(self, id_order):
        data_service = Database_Service()
        query = data_service.get_order_for_edit_db(id_order)
        if query.error is None:
            result = query.result
            if result:
                query = data_service.get_dishes_from_order_db(id_order)
                if query.error is None:
                    dishes_result = query.result
                    if dishes_result:
                        dishes = [Dish(
                            id_dish=row[0],
                            dish_name=row[1],
                            price=row[2],
                            weight=row[3],
                            photo=row[4],
                            menu_category=row[5],
                            dish_status=row[6],
                            amount=row[7])
                            for row in dishes_result]
                    order = Order(
                        id_order=result[0],
                        order_num=result[1],
                        worker=User(
                            id_worker=result[2],
                            role=0, job=None, last_name=None, first_name=None, middle_name=None, birth_date=None, address=None, phone_number=None, salary=0, login=None, password=None),
                        dishes=dishes,
                        table=result[3],
                        order_date=result[4],
                        order_time=result[5],
                        order_status=result[6])
                    return order
            return None
        else:
            return None