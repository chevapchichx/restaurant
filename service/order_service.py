from data.order_data import *
from service.database_service import *
from service.singleton import *

class Order_Service(metaclass=SingletonMeta):

    def fill_orders(self, login, role):
        data_service = Database_Service()
        query = data_service.get_orders_db(login, role)
        if query.error is None:
            result = query.result   
            if result:
                orders = [Order(
                    id_order=row[0],
                    order_num=row[1],
                    worker=User(
                        role=row[2],
                        job=row[3],
                        last_name=row[4],
                        first_name=row[5],
                        middle_name=row[6],
                        birth_date=row[7],
                        address=row[8],
                        phone_number=row[9],
                        salary=row[10],
                        login=row[11],
                        password=row[12]),
                    meal=row[13],
                    table=row[14],
                    order_date=row[15],
                    order_time=row[16],
                    price=row[17],
                    status=row[18])
                    for row in result]
                return orders
            else:
                return "Заказы не найдены"
        else:
            return f"Ошибка подключения к базе данных: {query.error}"

    def fill_order_by_id(self, id_order):
        data_service = Database_Service()
        query = data_service.get_order_by_id_db(id_order)
        if query.error is None:
            result = query.result
            if result:
                order = Order(
                    id_order=result[0],
                    order_num=result[1],
                    worker=User(
                        role=result[2],
                        job=result[3],
                        last_name=result[4],
                        first_name=result[5],
                        middle_name=result[6],
                        birth_date=result[7],
                        address=result[8],
                        phone_number=result[9],
                        salary=result[10],
                        login=result[11],
                        password=result[12]),
                    meal=result[13],
                    table=result[14],
                    order_date=result[15],
                    order_time=result[16],
                    price=result[17],
                    status=result[18])
                return order
            else:
                return "Заказ не найден"
        else:
            return f"Ошибка подключения к базе данных: {query.error}"