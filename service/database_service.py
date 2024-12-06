from sqlalchemy import create_engine, text
import os
from data.query_result_data import *
from data.user_data import User_Role
import configparser

config = configparser.ConfigParser()
config.read(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'config.txt'))
db_url = config['database']['db_url']

class Database_Service():
    __engine = create_engine(db_url)

    def get_user_db(self, login):
        try:
            with self.__engine.connect() as conn:
                query = text("""
                    SELECT id, role, job, last_name, first_name, middle_name, birth_date, address, phone_number, salary, login, password
                    FROM staff 
                    WHERE login = :login""")
                result = conn.execute(query, {"login": login}).fetchone()
                return Query_Result(result, None)
        except Exception as e:
            return Query_Result(None, e)
    
    def get_orders_db(self, id_worker, role):
        try:
            with self.__engine.connect() as conn:
                if role == User_Role.ADMIN:
                    query = text("""
                        SELECT o.id, o.order_num, o.guests, s.id, s.role, s.job, s.last_name, s.first_name, s.middle_name, o.id_table, o.order_date, o.order_time, o.order_status
                        FROM orders o
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
                return Query_Result(result, None)
        except Exception as e:
            return Query_Result(None, e)

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
                    SELECT m.id, m.dish, m.price, m.weight, m.id_menu_category, mc.category, o_m.dish_status, o_m.amount
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
    
    def create_new_order_db(self, id_worker):
        try:
            with self.__engine.begin() as conn:
                query = text("""
                    INSERT INTO orders (id_worker, order_date, order_time, guests)
                    VALUES (:id_worker, CURDATE(), CURTIME(), 0)
                """)
                conn.execute(query, {"id_worker": id_worker})

                select_query = text("SELECT LAST_INSERT_ID() AS last_id")
                result = conn.execute(select_query).fetchone()
                order_id = result[0]  

                get_max_order_num_query = text("SELECT MAX(order_num) FROM orders where order_status < 4")
                result = conn.execute(get_max_order_num_query).fetchone()
                order_num = result[0] + 1
                if order_num > 100:
                    order_num = 1

                update_query = text("""
                    UPDATE orders
                    SET order_num = :order_num
                    WHERE id = :order_id
                """)
                conn.execute(update_query, {
                    "order_id": order_id, 
                    "order_num": order_num
                    })
                result = conn.execute(text("SELECT id, order_num FROM orders WHERE id = :order_id"), {"order_id": order_id}).fetchone()
                return Query_Result(result, None)
        except Exception as e:
            return Query_Result(None, e)

    def get_is_table_occupied_db(self, table_id):
        try:
            with self.__engine.connect() as conn:
                query = text("""
                    SELECT COUNT(*)
                    FROM orders
                    WHERE id_table = :table_id AND order_status != 3
                """)
                result = conn.execute(query, {"table_id": table_id}).fetchone()
                return Query_Result(result[0] > 0, None)
        except Exception as e:
            return Query_Result(None, e)

    def get_table_capacity_db(self, table_id):
        try:
            with self.__engine.connect() as conn:
                query = text("""
                    SELECT number_of_seats
                    FROM tables
                    WHERE id = :table_id
                """)
                result = conn.execute(query, {"table_id": table_id}).fetchone()
                return Query_Result(result[0], None)
        except Exception as e:
            return Query_Result(None, e)
    
    def add_order_db(self, id_order, table_id, guests):
        try:
            with self.__engine.begin() as conn:
                update_query = text("""
                    UPDATE orders
                    SET id_table = :table_id, guests = :guests
                    WHERE id = :id_order
                """)
                conn.execute(update_query, {
                    "table_id": table_id,
                    "guests": guests,
                    "id_order": id_order
                })
                select_query = text("SELECT id, order_num, guests, id_worker, id_table, order_date, order_time, order_status FROM orders WHERE id = :id_order")
                result = conn.execute(select_query, {"id_order": id_order}).fetchone()
            return Query_Result(result, None)
        except Exception as e:
            return Query_Result(None, e)
    
    def update_dish_amount_db(self, order):
        try:
            with self.__engine.begin() as conn:
                update_query = text("""
                    UPDATE orders_menu 
                    SET amount = :amount, dish_status = 2 
                    WHERE id_dish = :id_dish AND id_order = :id_order
                """)
                for dish in order.dishes:
                    conn.execute(update_query, {
                        "amount": dish.amount,
                        "id_dish": dish.id_dish,
                        "id_order": order.id_order
                    })
                    print(f"Updated dish: {dish.dish_name}, amount: {dish.amount}")
                return Query_Result(None, None)
        except Exception as e:
            print(f"Error updating order: {e}")
            return Query_Result(None, e)
    
    def delete_dish_db(self, dish, id_order):
        try:
            with self.__engine.begin() as conn:
                query = text("""
                    DELETE FROM orders_menu
                    WHERE id IN (
                        SELECT id FROM (
                            SELECT id FROM orders_menu
                            WHERE id_dish = :id_dish AND dish_status = 1 AND id_order = :id_order
                            LIMIT 1
                        ) AS s
                    )
                """)
                conn.execute(query, {"id_dish": dish.id_dish, "id_order": id_order})
                return Query_Result(None, None)
        except Exception as e:
            return Query_Result(None, e)
        
    def get_menu_categories_db(self):
        try:
            with self.__engine.connect() as conn:
                query = text("""
                    SELECT category
                    FROM menu_category
                """)
                result = conn.execute(query).fetchall()
                return Query_Result(result, None)
        except Exception as e:
            return Query_Result(None, e)

    def get_dishes_by_category_db(self, category):
        try:
            with self.__engine.connect() as conn:
                query = text("""
                    SELECT id, dish, price, weight, id_menu_category
                    FROM menu
                    WHERE id_menu_category = (
                        SELECT id
                        FROM menu_category
                        WHERE category = :category
                    )
                """)
                result = conn.execute(query, {"category": category}).fetchall()
                return Query_Result(result, None)
        except Exception as e:
            return Query_Result(None, e)
    
    def get_dish_by_name_db(self, dish_name):
        try:
            with self.__engine.connect() as conn:
                query = text("""
                    SELECT id, dish, price, weight, id_menu_category
                    FROM menu 
                    WHERE dish = :dish_name
                """)
                result = conn.execute(query, {"dish_name": dish_name}).fetchone()
                return Query_Result(result, None)
        except Exception as e:
            return Query_Result(None, e)
    
    def add_dish_to_order_db(self, id_order, id_dish):
        try:
            with self.__engine.begin() as conn:
                query = text("""
                    INSERT INTO orders_menu (id_order, id_dish, amount, dish_status)
                    VALUES (:id_order, :id_dish, 1, 1)
                """)
                conn.execute(query, {
                    "id_order": id_order,
                    "id_dish": id_dish
                })
                return Query_Result(None, None)
        except Exception as e:
            return Query_Result(None, e)


