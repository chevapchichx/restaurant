import sys
import os
from data.order_data import *
from data.user_data import User
from service.database_service import *
from service.singleton import *
from data.dish_data import *
from data.menu_category_data import *
from data.table_data import *
from PyQt6.QtWidgets import QMessageBox

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
                    guests=row[2],
                    worker=User(
                        id_worker=row[3],
                        role=row[4],
                        job=row[5],
                        last_name=row[6],
                        first_name=row[7],
                        middle_name=row[8],
                        birth_date=None, address=None, phone_number=None, salary=0, login=None, password=None),
                    table=row[9],
                    order_date=row[10],
                    order_time=row[11],
                    order_status=row[12],
                    dishes=[],
                    total_sum=0)
                    for row in result]
                return orders
            else:
                QMessageBox.critical(None, "Ошибка", "Заказы не найдены")
                return None
        else:
            QMessageBox.critical(None, "Ошибка", f"Ошибка подключения к базе данных: {query.error}")
            return None

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
                        dishes = []
                        total_sum = 0
                        for row in dishes_result:
                            dish_sum = row[2] * row[8] 
                            total_sum += dish_sum 
                            dish = Dish(
                                id_dish=row[0],
                                dish_name=row[1],
                                price=row[2],
                                weight=row[3],
                                photo=row[4],
                                menu_category=[Menu_Category(
                                    id_menu_category=row[5],
                                    category=row[6])],
                                dish_status=row[7],
                                amount=row[8],
                                dish_sum=dish_sum) 
                            dishes.append(dish)
                    order = Order(
                        id_order=result[0],
                        order_num=result[1],
                        guests=result[2],
                        worker=User(
                            id_worker=result[3],
                            role=0, job=None, last_name=None, first_name=None, middle_name=None, birth_date=None, address=None, phone_number=None, salary=0, login=None, password=None),
                        dishes=dishes,
                        table=Table(
                            id_table=result[4],
                            number_of_seats=result[5]),
                        order_date=result[6],
                        order_time=result[7],
                        order_status=result[8],
                        total_sum=total_sum)
                    return order
            QMessageBox.critical(None, "Ошибка", "Заказ не найден")
            return None
        else:
            QMessageBox.critical(None, "Ошибка", f"Ошибка подключения к базе данных: {query.error}")
            return None