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
                query = data_service.get_items_from_order_db(id_order)
                if query.error is None:
                    order_items_result = query.result
                    dishes = []
                    order_items = []
                    if order_items_result:
                        for row in order_items_result:
                            dish = Dish(
                                id_dish=row[0],
                                dish_name=row[1],
                                price=row[2],
                                weight=row[3],
                                menu_category=[Menu_Category(
                                    id_menu_category=row[4],
                                    name=row[5])]) 
                            dishes.append(dish)
                            order_item = Order_Item(
                                id_order_item=row[6],
                                dish=dish,
                                amount=row[7],
                                status=row[8]
                            )
                            order_items.append(order_item)
                    order = Order(
                        id_order=result[0],
                        order_num=result[1],
                        guests=result[2],
                        worker=User(
                            id_worker=result[3],
                            role=0, job=None, last_name=None, first_name=None, middle_name=None, birth_date=None, address=None, phone_number=None, salary=0, login=None, password=None),
                        table=Table(
                            id_table=result[4],
                            number_of_seats=result[5]),
                        order_date=result[6],
                        order_time=result[7],
                        order_status=result[8],
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
                    order_items=[]
                    )
                return order
            else:
                QMessageBox.critical(None, "Ошибка", "Не удалось добавить заказ")
                return None
        else:
            QMessageBox.critical(None, "Ошибка", f"Ошибка подключения к базе данных: {query.error}")
            return None
    
    def delete_order_item(self, order_item, id_order):
        data_service = Database_Service()
        query = data_service.delete_order_item_db(order_item, id_order)
        if query.error is None:
            return True
        else:
            QMessageBox.critical(None, "Ошибка", f"Ошибка подключения к базе данных: {query.error}")
            return None
    
    def add_dish_to_order(self, id_order, dish):
        data_service = Database_Service()
        query = data_service.add_dish_to_order_db(id_order, dish)
        if query.error is None:
            result = query.result
            return result[0]
        else:
            QMessageBox.critical(None, "Ошибка", f"Ошибка подключения к базе данных: {query.error}")
            return None
    
    def get_order_item_by_id(self, id_order_item):
        data_service = Database_Service()
        query = data_service.get_order_item_by_id_db(id_order_item)
        if query.error is None:
            result = query.result
            if result:
                dish = Dish(
                    id_dish=result[0],
                    dish_name=result[1],
                    price=result[2],
                    weight=result[3],
                    menu_category=[Menu_Category(
                        id_menu_category=result[4],
                        name=result[5])])
                order_item = Order_Item(
                    id_order_item=result[6],
                    dish=dish,
                    amount=result[7],
                    status=result[8]
                )
                return order_item
            else:
                QMessageBox.critical(None, "Ошибка", "Блюдо не найдено")
                return None
        else:
            QMessageBox.critical(None, "Ошибка", f"Ошибка подключения к базе данных: {query.error}")
            return None
    
    def update_order_item_amount(self, order_item):
        data_service = Database_Service()
        query = data_service.update_order_item_amount_db(order_item)
        if query.error is None:
            return True
        else:
            QMessageBox.critical(None, "Ошибка", f"Ошибка подключения к базе данных: {query.error}")
            return None
    
    def update_order_item_status(self, order, status):
        data_service = Database_Service()
        query = data_service.update_order_item_status_db(order, status)
        if query.error is None:
            return True
        else:
            QMessageBox.critical(None, "Ошибка", f"Ошибка подключения к базе данных: {query.error}")
            return None
    
