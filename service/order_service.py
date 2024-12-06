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
from data.order_item_data import Order_Item

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
                    total_sum=0,
                    order_items=[])
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
                    dishes = []
                    order_items = []
                    total_sum = 0
                    if dishes_result:
                        for row in dishes_result:
                            dish_sum = row[2] * row[7] 
                            total_sum += dish_sum 
                            dish = Dish(
                                id_dish=row[0],
                                dish_name=row[1],
                                price=row[2],
                                weight=row[3],
                                menu_category=[Menu_Category(
                                    id_menu_category=row[4],
                                    category=row[5])],
                                dish_status=row[6],
                                amount=row[7],
                                dish_sum=dish_sum) 
                            dishes.append(dish)
                            order_item = Order_Item(
                                id_order_item=0,
                                dish=dish,
                                amount=row[7],
                                status=row[6]
                            )
                            order_items.append(order_item)
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
                        total_sum=total_sum,
                        order_items=order_items)
                    return order
            QMessageBox.critical(None, "Ошибка", "Заказ не найден")
            return None
        else:
            QMessageBox.critical(None, "Ошибка", f"Ошибка подключения к базе данных: {query.error}")
            return None

    def create_new_order(self, id_worker):
        data_service = Database_Service()
        query = data_service.create_new_order_db(id_worker)
        if query.error is None:
            result = query.result
            return result
        else:
            QMessageBox.critical(None, "Ошибка", f"Ошибка подключения к базе данных: {query.error}")
            return None

    def get_is_table_occupied(self, table_id):
        data_service = Database_Service()
        query = data_service.get_is_table_occupied_db(table_id)
        if query.error is None:
            result = query.result
            return result
        else:
            QMessageBox.critical(None, "Ошибка", f"Ошибка подключения к базе данных: {query.error}")
            return None

    def get_table_capacity(self, table_id):
        data_service = Database_Service()
        query = data_service.get_table_capacity_db(table_id)
        if query.error is None:
            return query.result
        else:
            QMessageBox.critical(None, "Ошибка", f"Ошибка подключения к базе данных: {query.error}")
            return None
    
    def add_order(self, id_order, table_id, guests):
        data_service = Database_Service()
        query = data_service.add_order_db(id_order, table_id, guests)
        if query.error is None:
            result = query.result
            if result:
                order = Order(
                    id_order=result[0],
                    order_num=result[1],
                    guests=result[2],
                    worker=User(
                        id_worker=result[3],
                        role=0, job=None, last_name=None, first_name=None, middle_name=None, birth_date=None, address=None, phone_number=None, salary=0, login=None, password=None),
                    table=Table(
                        id_table=result[4],
                        number_of_seats=0),
                    order_date=result[5],
                    order_time=result[6],
                    order_status=result[7],
                    dishes=[],
                    total_sum=0,
                    order_items=[])
                return order
            else:
                QMessageBox.critical(None, "Ошибка", "Не удалось добавить заказ")
                return None
        else:
            QMessageBox.critical(None, "Ошибка", f"Ошибка подключения к базе данных: {query.error}")
            return None
    
    def update_dish_amount(self, order):
        data_service = Database_Service()
        query = data_service.update_dish_amount_db(order)
        if query.error is None:
            return True
        else:
            QMessageBox.critical(None, "Ошибка", f"Ошибка подключения к базе данных: {query.error}")
            return None
    
    def delete_dish(self, dish, id_order):
        data_service = Database_Service()
        query = data_service.delete_dish_db(dish, id_order)
        if query.error is None:
            return True
        else:
            QMessageBox.critical(None, "Ошибка", f"Ошибка подключения к базе данных: {query.error}")
            return None
    
    def add_dish_to_order(self, id_order, id_dish):
        data_service = Database_Service()
        query = data_service.add_dish_to_order_db(id_order, id_dish)
        if query.error is None:
            return True
        else:
            QMessageBox.critical(None, "Ошибка", f"Ошибка подключения к базе данных: {query.error}")
            return None