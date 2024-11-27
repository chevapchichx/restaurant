from sqlalchemy import create_engine, text
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from data.query_result_data import *
from data.user_data import User_Role 

class Database_Service():
    __engine = create_engine('mysql+mysqlconnector://root:root@localhost:8889/restaurant')

    def get_user_db(self, login):
        try:
            with self.__engine.connect() as conn:
                query = text("""
                    SELECT id, role, job, last_name, first_name, middle_name, birth_date, address, phone_number, salary, login, password
                    SELECT id, role, job, last_name, first_name, middle_name, birth_date, address, phone_number, salary, login, password
                    FROM staff 
                    WHERE login = :login""")
                result = conn.execute(query, {"login": login}).fetchone()
                return Query_Result(result, None)
        except Exception as e:
            return Query_Result(None, e)
    
    def get_orders_db(self, id_worker, role):
    def get_orders_db(self, id_worker, role):
        try:
            with self.__engine.connect() as conn:
                if role == User_Role.ADMIN:
                    query = text("""
                        SELECT o.id, o.order_num, o.guests, s.id, s.role, s.job, s.last_name, s.first_name, s.middle_name, o.id_table, o.order_date, o.order_time, o.order_status
                        FROM orders o
                        JOIN staff s ON o.id_worker = s.id
                        """)
                        JOIN staff s ON o.id_worker = s.id
                        """)
                    result = conn.execute(query).fetchall()
                else:
                    query = text("""
                        SELECT o.id, o.order_num, o.guests, s.id, s.role, s.job, s.last_name, s.first_name, s.middle_name, o.id_table, o.order_date, o.order_time, o.order_status
                        FROM orders o
                        JOIN staff s ON o.id_worker = s.id
                        WHERE o.id_worker = :id_worker
                        """)
                    result = conn.execute(query, {"id_worker": id_worker}).fetchall()
                        JOIN staff s ON o.id_worker = s.id
                        WHERE o.id_worker = :id_worker
                        """)
                    result = conn.execute(query, {"id_worker": id_worker}).fetchall()
                return Query_Result(result, None)
        except Exception as e:
            return Query_Result(None, e)

    def get_order_for_edit_db(self, id_order):
    def get_order_for_edit_db(self, id_order):
        try:
            with self.__engine.connect() as conn:
                query = text("""
                    SELECT o.id, o.order_num, o.guests, o.id_worker, o.id_table, t.number_of_seats, o.order_date, o.order_time, o.order_status
                        FROM orders o
                        JOIN tables t ON o.id_table = t.id
                    WHERE o.id = :id_order
                    """)
                result = conn.execute(query, {"id_order": id_order}).fetchone()
                return Query_Result(result, None)
        except Exception as e:
            return Query_Result(None, e)

    def get_dishes_from_order_db(self, id_order):
        try:
            with self.__engine.connect() as conn:
                query = text("""
                    SELECT m.id, m.dish, m.price, m.weight, m.photo, m.id_menu_category, mc.category, o_m.dish_status, o_m.amount
                    FROM orders o
                    JOIN orders_menu o_m ON o.id = o_m.id_order
                    JOIN menu m ON m.id = o_m.id_dish
                    JOIN menu_category mc ON m.id_menu_category = mc.id
                    WHERE o.id = :id_order
                    """)
                result = conn.execute(query, {"id_order": id_order}).fetchall()
                return Query_Result(result, None)
        except Exception as e:
            return Query_Result(None, e)
    
    # def get_meal_by_id_db(self, id_meal):
    #     try:
    #         with self.__engine.connect() as conn:
    #             query = text("""
    #                 SELECT m.id_meal, m.meal, m.price, m.weight, m.photo, m.id_menu_section
    #                 FROM menu m, orders o
    #                 WHERE o.id_meal = :id_meal""")
    #             result = conn.execute(query, {"id_meal": id_meal}).fetchone()
    #             return Query_Result(result, None)
    #     except Exception as e:
    #         return Query_Result(None, e)



