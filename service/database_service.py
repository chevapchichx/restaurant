import configparser
import os
from sqlalchemy import create_engine, text

from data.query_result_data import QueryResult 
from data.user_data import UserRole
from data.order_item_data import DishStatus


config = configparser.ConfigParser()
config.read(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'config.txt'))
db_url = config['database']['db_url']


class DatabaseService:
    __engine = create_engine(db_url)

    def get_user_db(self, login):
        try:
            with self.__engine.connect() as conn:
                query = text("""
                    SELECT id, role, job, last_name, first_name, middle_name, birth_date, address, phone_number, salary, login, password
                    FROM staff 
                    WHERE login = :login and deleted is null""")
                result = conn.execute(query, {"login": login}).fetchone()
                return QueryResult(result, None)
        except Exception as e:
            return QueryResult(None, e)
    
    def get_orders_db(self, id_staff, role):
        try:
            with self.__engine.connect() as conn:
                if (role == UserRole.ADMIN):
                    query = text("""
                        SELECT o.id, o.order_num, o.guests, o.id_staff, s.role, s.job, s.last_name, s.first_name, s.middle_name, o.id_table, o.order_date, o.order_time, o.order_status
                        FROM orders o
                        JOIN staff s ON o.id_staff = s.id
                        """)
                    result = conn.execute(query).fetchall()
                else:
                    query = text("""
                        SELECT o.id, o.order_num, o.guests, o.id_staff, s.role, s.job, s.last_name, s.first_name, s.middle_name, o.id_table, o.order_date, o.order_time, o.order_status
                        FROM orders o
                        JOIN staff s ON o.id_staff = s.id
                        WHERE o.id_staff = :id_staff
                        """)
                    result = conn.execute(query, {"id_staff": id_staff}).fetchall()
                return QueryResult(result, None)
        except Exception as e:
            return QueryResult(None, e)

    def get_order_for_edit_db(self, id_order):
        try:
            with self.__engine.connect() as conn:
                query = text("""
                    SELECT o.id, o.order_num, o.guests, o.id_staff, o.id_table, t.number_of_seats, o.order_date, o.order_time, o.order_status
                        FROM orders o
                        JOIN tables t ON o.id_table = t.id
                    WHERE o.id = :id_order
                    """)
                result = conn.execute(query, {"id_order": id_order}).fetchone()
                return QueryResult(result, None)
        except Exception as e:
            return QueryResult(None, e)

    def get_items_from_order_db(self, id_order):
        try:
            with self.__engine.connect() as conn:
                query = text("""
                    SELECT m.id, m.dish, m.price, m.weight, m.id_menu_category, mc.category, o_m.id, o_m.amount, o_m.dish_status, o_m.id_order
                    FROM orders o
                    JOIN orders_menu o_m ON o.id = o_m.id_order
                    JOIN menu m ON m.id = o_m.id_dish
                    JOIN menu_category mc ON m.id_menu_category = mc.id
                    WHERE o.id = :id_order
                    """)
                result = conn.execute(query, {"id_order": id_order}).fetchall()
                return QueryResult(result, None)
        except Exception as e:
            return QueryResult(None, e)
    
    def create_new_order_db(self, id_staff):
        try:
            with self.__engine.begin() as conn:
                query = text("""
                    INSERT INTO orders (id_staff, order_date, order_time, guests)
                    VALUES (:id_staff, CURDATE(), CURTIME(), 0)
                """)
                conn.execute(query, {"id_staff": id_staff})

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
                return QueryResult(result, None)
        except Exception as e:
            return QueryResult(None, e)

    def get_is_table_occupied_db(self, table_id):
        try:
            with self.__engine.connect() as conn:
                query = text("""
                    SELECT COUNT(*)
                    FROM orders
                    WHERE id_table = :table_id AND order_status != 4
                """)
                result = conn.execute(query, {"table_id": table_id}).fetchone()
                return QueryResult(result[0] > 0, None)
        except Exception as e:
            return QueryResult(None, e)

    def get_table_capacity_db(self, table_id):
        try:
            with self.__engine.connect() as conn:
                query = text("""
                    SELECT number_of_seats
                    FROM tables
                    WHERE id = :table_id
                """)
                result = conn.execute(query, {"table_id": table_id}).fetchone()
                return QueryResult(result[0], None)
        except Exception as e:
            return QueryResult(None, e)
    
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
                select_query = text("SELECT id, order_num, guests, id_staff, id_table, order_date, order_time, order_status FROM orders WHERE id = :id_order")
                result = conn.execute(select_query, {"id_order": id_order}).fetchone()
            return QueryResult(result, None)
        except Exception as e:
            return QueryResult(None, e)
    
    def update_order_item_amount_db(self, order_item):
        try:
            with self.__engine.begin() as conn:
                query = text("""
                    UPDATE orders_menu
                    SET amount = :amount
                    WHERE id = :id_order_item
                """)
                conn.execute(query, {
                    "amount": order_item.amount,
                    "id_order_item": order_item.id_order_item
                })
                return QueryResult(None, None)
        except Exception as e:
            return QueryResult(None, e)
    
    def delete_order_item_db(self, order_item, id_order):
        try:
            with self.__engine.begin() as conn:
                query = text("""
                    DELETE FROM orders_menu
                    WHERE id_order = :id_order AND id = :id_order_item
                """)
                conn.execute(query, {
                    "id_order": id_order,
                    "id_order_item": order_item.id_order_item
                })
                return QueryResult(None, None)
        except Exception as e:
            return QueryResult(None, e)
        
    def get_menu_categories_db(self):
        try:
            with self.__engine.connect() as conn:
                query = text("""
                    SELECT id, category
                    FROM menu_category
                """)
                result = conn.execute(query).fetchall()
                return QueryResult(result, None)
        except Exception as e:
            return QueryResult(None, e)

    def get_dishes_by_category_db(self, id_menu_category):
        try:
            with self.__engine.connect() as conn:
                query = text("""
                    SELECT id, dish, price, weight, id_menu_category
                    FROM menu
                    WHERE id_menu_category = :id_menu_category
                """)
                result = conn.execute(query, {"id_menu_category": id_menu_category}).fetchall()
                return QueryResult(result, None)
        except Exception as e:
            return QueryResult(None, e)
    
    def get_dish_by_id_db(self, id_dish):
        try:
            with self.__engine.connect() as conn:
                query = text("""
                    SELECT id, dish, price, weight, id_menu_category
                    FROM menu 
                    WHERE id = :id_dish
                """)
                result = conn.execute(query, {"id_dish": id_dish}).fetchone()
                return QueryResult(result, None)
        except Exception as e:
            return QueryResult(None, e)
    
    def add_dish_to_order_db(self, id_order, dish):
        try:
            with self.__engine.begin() as conn:
                query = text("""
                    INSERT INTO orders_menu (id_order, id_dish, amount, dish_status)
                    VALUES (:id_order, :id_dish, 1, 1)
                """)
                conn.execute(query, {
                    "id_order": id_order,
                    "id_dish": dish.id_dish
                })
                result = conn.execute(text("SELECT LAST_INSERT_ID() AS last_id")).fetchone()
                return QueryResult(result, None)
        except Exception as e:
            return QueryResult(None, e)
    
    def get_order_item_by_id_db(self, id_order_item):
        try:
            with self.__engine.connect() as conn:
                query = text("""
                    SELECT m.id, m.dish, m.price, m.weight, m.id_menu_category, mc.category, o_m.id, o_m.amount, o_m.dish_status, o_m.id_order
                    FROM menu m
                    JOIN orders_menu o_m ON m.id = o_m.id_dish
                    JOIN menu_category mc ON m.id_menu_category = mc.id
                    WHERE o_m.id = :id_order_item
                """)
                result = conn.execute(query, {"id_order_item": id_order_item}).fetchone()
                return QueryResult(result, None)
        except Exception as e:
            return QueryResult(None, e)
    
    def update_order_items_status_db(self, order, status):
        try:
            with self.__engine.begin() as conn:
                query = text("""
                    UPDATE orders_menu
                    SET dish_status = :status
                    WHERE id_order = :id_order
                """)
                conn.execute(query, {
                    "status": status,
                    "id_order": order.id_order
                })
                return QueryResult(None, None)
        except Exception as e:
            return QueryResult(None, e)
    
    def get_order_items_db(self):
        try:
            with self.__engine.connect() as conn:
                query = text("""
                    SELECT o_m.id, o_m.id_dish, m.dish, m.price, m.weight, m.id_menu_category, mc.category, 
                             o_m.amount, o_m.dish_status, o_m.id_order
                    FROM orders_menu o_m
                    JOIN menu m ON o_m.id_dish = m.id
                    JOIN menu_category mc ON m.id_menu_category = mc.id
                    """)
                result = conn.execute(query).fetchall()
                return QueryResult(result, None)
        except Exception as e:
            return QueryResult(None, e)
        
    def update_order_item_status_db(self, order_item, status):
        try:
            with self.__engine.begin() as conn:
                query = text("""
                    UPDATE orders_menu
                    SET dish_status = :status
                    WHERE id = :id_order_item
                """)
                conn.execute(query, {
                    "status": status,
                    "id_order_item": order_item.id_order_item
                })
                return QueryResult(None, None)
        except Exception as e:
            return QueryResult(None, e)
    
    def update_order_status_db(self, order, status):
        try:
            with self.__engine.begin() as conn:
                query = text("""
                    UPDATE orders
                    SET order_status = :status
                    WHERE id = :id_order
                """)
                conn.execute(query, {
                    "status": status,
                    "id_order": order.id_order
                })
                return QueryResult(None, None)
        except Exception as e:
            return QueryResult(None, e)

    def get_staffs_info_db(self):
        try:
            with self.__engine.connect() as conn:
                query = text("""
                    SELECT id, role, job, last_name, first_name, middle_name, birth_date, address, phone_number, salary
                    FROM staff
                    where deleted is null
                """)
                result = conn.execute(query).fetchall()
                return QueryResult(result, None)
        except Exception as e:
            return QueryResult(None, e)

    def check_exist_login_db(self, login):
        try:
            with self.__engine.connect() as conn:
                query = text("""
                    SELECT id, last_name, first_name, middle_name, login, password, 
                    case
                        when deleted is null then 1
                        when deleted is not null then 0
                    end as is_exist
                    FROM staff 
                    WHERE login = :login
                """)
                result = conn.execute(query, {"login": login}).fetchone()
                return QueryResult(result, None)
        except Exception as e:
            return QueryResult(None, e)
        
    def update_deleted_status_staff_db(self, id_staff):
        try:
            with self.__engine.begin() as conn:
                query = text("""
                    UPDATE staff
                    set deleted = CASE 
                        when deleted is null then CURRENT_TIMESTAMP()
                        else null
                        end
                    where id = :id_staff
                """)
                conn.execute(query, {"id_staff": id_staff})
                return QueryResult(None, None)
        except Exception as e:
            return QueryResult(None, e)
    
    def add_staff_db(self, login, password, role, last_name, first_name, middle_name, job, birth_date, address, phone_number, salary):
        try:
            with self.__engine.begin() as conn:
                query = text("""
                    INSERT INTO staff (login, password, role, last_name, first_name, middle_name, job, birth_date, address, phone_number, salary)
                    VALUES (:login, :password, :role, :last_name, :first_name, :middle_name, :job, :birth_date, :address, :phone_number, :salary)
                """)
                conn.execute(query, {
                    "login": login,
                    "password": password,
                    "role": role,
                    "last_name": last_name,
                    "first_name": first_name,
                    "middle_name": middle_name,
                    "job": job,
                    "birth_date": birth_date,
                    "address": address,
                    "phone_number": phone_number,
                    "salary": salary
                })
                return QueryResult(None, None)
        except Exception as e:
            return QueryResult(None, e)
    
    def update_staff_db(self, login, password, role, last_name, first_name, middle_name, job, birth_date, address, phone_number, salary):
        try:
            with self.__engine.begin() as conn:
                query = text("""
                    UPDATE staff
                    SET password = :password, role = :role, last_name = :last_name, first_name = :first_name, middle_name = :middle_name, job = :job, birth_date = :birth_date, address = :address, phone_number = :phone_number, salary = :salary
                    WHERE login = :login
                """)
                conn.execute(query, {
                    "login": login,
                    "password": password,
                    "role": role,
                    "last_name": last_name,
                    "first_name": first_name,
                    "middle_name": middle_name,
                    "job": job,
                    "birth_date": birth_date,
                    "address": address,
                    "phone_number": phone_number,
                    "salary": salary
                })
                return QueryResult(None, None)
        except Exception as e:
            return QueryResult(None, e)
        

                
        



