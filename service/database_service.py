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
                    SELECT role, job, last_name, first_name, middle_name, birth_date, address, phone_number, salary, login, password
                    FROM staff 
                    WHERE login = :login""")
                result = conn.execute(query, {"login": login}).fetchone()
                return Query_Result(result, None)
        except Exception as e:
            return Query_Result(None, e)
    
    def get_orders_db(self, login, role):
        try:
            with self.__engine.connect() as conn:
                if role == User_Role.ADMIN:
                    query = text("""
                        SELECT o.id_order, o.order_num, s.role, s.job, s.last_name, s.first_name, s.middle_name, s.birth_date, s.address, s.phone_number, s.salary, s.login, s.password, o.id_meal, o.id_table, o.order_date, o.order_time, o.price, o.order_status
                        FROM orders o
                        JOIN staff s ON o.id_worker = s.login""")
                    result = conn.execute(query).fetchall()
                else:
                    query = text("""
                        SELECT o.id_order, o.order_num, s.role, s.job, s.last_name, s.first_name, s.middle_name, s.birth_date, s.address, s.phone_number, s.salary, s.login, s.password, o.id_meal, o.id_table, o.order_date, o.order_time, o.price, o.order_status
                        FROM orders o
                        JOIN staff s ON o.id_worker = s.login
                        WHERE o.id_worker = :worker""")
                    result = conn.execute(query, {"worker": login}).fetchall()
                return Query_Result(result, None)
        except Exception as e:
            return Query_Result(None, e)

    def get_order_by_id_db(self, id_order):
        try:
            with self.__engine.connect() as conn:
                query = text("""
                    SELECT o.id_order, o.order_num, s.role, s.job, s.last_name, s.first_name, s.middle_name, s.birth_date, s.address, s.phone_number, s.salary, s.login, s.password, o.id_meal, o.id_table, o.order_date, o.order_time, o.price, o.order_status
                    FROM orders o
                    JOIN staff s ON o.id_worker = s.login
                    WHERE o.id_order = :id_order""")
                result = conn.execute(query, {"id_order": id_order}).fetchone()
                return Query_Result(result, None)
        except Exception as e:
            return Query_Result(None, e)




