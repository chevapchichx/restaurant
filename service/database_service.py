import configparser
import os
from sqlalchemy import create_engine, text

from data.query_result_data import QueryResult
from data.user_data import UserRole
from data.order_data import OrderStatus

# config = configparser.configparser()
# config.read(os.path.join(os.path.dirname(
#     os.path.dirname(os.path.abspath(__file__))), 'config.txt'))
db_url = "mysql+pymysql://root:root@localhost/restaurant"


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
                    result = conn.execute(
                        query, {"id_staff": id_staff}).fetchall()
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
                    SELECT m.id, m.dish, m.price, m.weight, m.id_menu_category, mc.category, o_m.id, o_m.amount, o_m.dish_status, o_m.id_order, o_m.added_time
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
        """
        Создает новый заказ в базе данных.

        Аргументы:
        id_staff - идентификатор сотрудника, создающего заказ

        Возвращает:
        QueryResult - объект, содержащий результат выполнения запроса и возможную ошибку
        """
        try:
            with self.__engine.begin() as conn:  # Начинается транзакция
                # SQL-запрос для вставки нового заказа в таблицу orders
                query = text("""
                    INSERT INTO orders (id_staff, order_date, order_time, guests)
                    VALUES (:id_staff, CURDATE(), CURTIME(), 0)
                """)
                conn.execute(query, {"id_staff": id_staff}
                             )  # Выполняется запрос, передавая id_staff

                # SQL-запрос для получения последнего вставленного идентификатора заказа
                select_query = text("SELECT LAST_INSERT_ID() AS last_id")
                # Выполняется запрос, получаем результат
                result = conn.execute(select_query).fetchone()
                order_id = result[0]  # Извлекается идентификатор заказа

                # SQL-запрос для получения максимального номера заказа, который еще не закрыт
                get_max_order_num_query = text(
                    "SELECT MAX(order_num) FROM orders where order_status < 4")
                # Выполняется запрос, получаем результат
                result = conn.execute(get_max_order_num_query).fetchone()
                order_num = result[0]  # Извлекается максимальный номер заказа

                # Если максимальный номер заказа равен None или больше 100, устанавливается в 1
                if order_num is None or order_num > 100:
                    order_num = 1
                else:
                    order_num += 1  # Иначе увеличивается номер заказа на 1

                # SQL-запрос для обновления номера заказа и статуса заказа
                update_query = text("""
                    UPDATE orders
                    SET order_num = :order_num, order_status = :order_status
                    WHERE id = :order_id
                """)
                # Выполняется запрос, передавая order_id, order_num и статус заказа
                conn.execute(update_query, {
                    "order_id": order_id,
                    "order_num": order_num,
                    "order_status": OrderStatus.CREATED
                })

                # SQL-запрос для получения идентификатора и номера заказа
                result = conn.execute(text("SELECT id, order_num FROM orders WHERE id = :order_id"), {
                                      "order_id": order_id}).fetchone()
                # Возвращается результат выполнения запроса
                return QueryResult(result, None)
        except Exception as e:
            # В случае ошибки возвращается объект QueryResult с ошибкой
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
                select_query = text("""SELECT id, order_num, guests, id_staff, id_table, order_date, 
                                    order_time, order_status FROM orders WHERE id = :id_order
                                    """)
                result = conn.execute(
                    select_query, {"id_order": id_order}).fetchone()
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
                result = conn.execute(
                    query, {"id_menu_category": id_menu_category}).fetchall()
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
                    INSERT INTO orders_menu (id_order, id_dish, amount, dish_status, added_time)
                    VALUES (:id_order, :id_dish, 1, 1, NOW())
                """)
                conn.execute(query, {
                    "id_order": id_order,
                    "id_dish": dish.id_dish
                })
                result = conn.execute(
                    text("SELECT LAST_INSERT_ID() AS last_id")).fetchone()
                return QueryResult(result, None)
        except Exception as e:
            return QueryResult(None, e)

    def get_order_item_by_id_db(self, id_order_item):
        try:
            with self.__engine.connect() as conn:
                query = text("""
                    SELECT m.id, m.dish, m.price, m.weight, m.id_menu_category, mc.category, o_m.id, o_m.amount, o_m.dish_status, o_m.id_order, o_m.added_time
                    FROM menu m
                    JOIN orders_menu o_m ON m.id = o_m.id_dish
                    JOIN menu_category mc ON m.id_menu_category = mc.id
                    WHERE o_m.id = :id_order_item
                """)
                result = conn.execute(
                    query, {"id_order_item": id_order_item}).fetchone()
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
                    and dish_status != 3
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
                             o_m.amount, o_m.dish_status, o_m.id_order, o_m.added_time
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
                    SELECT id, role, job, last_name, first_name, middle_name, birth_date, address, phone_number, salary, login
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

    def check_or_update_order_items_status_in_order_db(self, id_order):
        try:
            with self.__engine.begin() as conn:
                query = text("""
                    UPDATE orders o
                    SET o.order_status = 3
                    WHERE o.id= :id_order
                    AND NOT EXISTS (
                        SELECT 1
                        FROM orders_menu o_m
                        WHERE o_m.id_order = o.id
                        AND o_m.dish_status != 3
                    )
                """)
                conn.execute(query, {"id_order": id_order})
                return QueryResult(None, None)
        except Exception as e:
            return QueryResult(None, e)

    def get_today_stats_db(self):
        try:
            with self.__engine.connect() as conn:
                query = text("""
                    SELECT 
                        (SELECT COUNT(*) FROM orders 
                         WHERE DATE(order_date) = CURDATE()
                         AND order_status = 4) as completed_orders_count,
                        (SELECT AVG(order_sum) 
                             FROM (
                                SELECT o.id, SUM(om.amount * m.price) as order_sum
                                FROM orders o
                                JOIN orders_menu om ON o.id = om.id_order
                                JOIN menu m ON om.id_dish = m.id
                                WHERE DATE(o.order_date) = CURDATE()
                                AND o.order_status = 4
                                GROUP BY o.id
                             ) as daily_orders
                        ) as avg_order,
                        (SELECT SUM(order_sum)
                             FROM (
                                SELECT o.id, SUM(om.amount * m.price) as order_sum
                                FROM orders o
                                JOIN orders_menu om ON o.id = om.id_order
                                JOIN menu m ON om.id_dish = m.id
                                WHERE DATE(o.order_date) = CURDATE()
                                AND o.order_status = 4
                                GROUP BY o.id
                             ) as daily_totals
                        ) as total_revenue
                """)
                result = conn.execute(query).fetchone()
                return QueryResult(result, None)
        except Exception as e:
            return QueryResult(None, e)

    def get_popular_dishes_db(self):
        try:
            with self.__engine.connect() as conn:
                query = text("""
                    SELECT 
                        m.id,
                        m.dish,
                        SUM(om.amount) as total_count,
                        SUM(om.amount * m.price) as total_sum
                    FROM orders_menu om
                    JOIN menu m ON om.id_dish = m.id
                    JOIN orders o ON om.id_order = o.id
                    WHERE DATE(o.order_date) = CURDATE()
                    AND o.order_status = 4
                    GROUP BY m.id, m.dish
                    ORDER BY total_count DESC
                """)
                result = conn.execute(query).fetchall()
                return QueryResult(result, None)
        except Exception as e:
            return QueryResult(None, e)

    def update_password_db(self, login, password):
        try:
            with self.__engine.begin() as conn:
                query = text("""
                    UPDATE staff
                    SET password = :password
                    WHERE login = :login
                """)
                conn.execute(query, {
                    "login": login,
                    "password": password
                })
                return QueryResult(None, None)
        except Exception as e:
            return QueryResult(None, e)

    def get_all_dishes_db(self):
        try:
            with self.__engine.connect() as conn:
                query = text("""
                    SELECT m.id, m.dish, m.price, m.weight, m.id_menu_category
                    FROM menu m
                    ORDER BY m.dish
                """)
                result = conn.execute(query).fetchall()
                return QueryResult(result, None)
        except Exception as e:
            return QueryResult(None, e)

    def add_dish_db(self, dish_name, price, weight, category_id):
        try:
            with self.__engine.begin() as conn:
                query = text("""
                    INSERT INTO menu (dish, price, weight, id_menu_category)
                    VALUES (:dish_name, :price, :weight, :category_id)
                """)
                conn.execute(query, {
                    "dish_name": dish_name,
                    "price": price,
                    "weight": weight,
                    "category_id": category_id
                })
                return QueryResult(True, None)
        except Exception as e:
            return QueryResult(None, e)

    def get_reservations_db(self, date=None):
        try:
            with self.__engine.connect() as conn:
                if date:
                    query = text("""
                        SELECT id, customer_name, phone_number, guests, 
                               reservation_date, reservation_time, id_table, status, notes
                        FROM reservations
                        WHERE reservation_date = :date
                        ORDER BY reservation_time
                    """)
                    result = conn.execute(query, {"date": date}).fetchall()
                else:
                    query = text("""
                        SELECT id, customer_name, phone_number, guests, 
                               reservation_date, reservation_time, id_table, status, notes
                        FROM reservations
                        WHERE reservation_date >= CURDATE()
                        ORDER BY reservation_date, reservation_time
                    """)
                    result = conn.execute(query).fetchall()
                return QueryResult(result, None)
        except Exception as e:
            return QueryResult(None, e)

    def add_reservation_db(self, reservation):
        try:
            with self.__engine.begin() as conn:
                query = text("""
                    INSERT INTO reservations 
                    (customer_name, phone_number, guests, reservation_date, 
                     reservation_time, id_table, status, notes)
                    VALUES 
                    (:customer_name, :phone_number, :guests, :reservation_date, 
                     :reservation_time, :id_table, :status, :notes)
                """)
                conn.execute(query, {
                    "customer_name": reservation.customer_name,
                    "phone_number": reservation.phone_number,
                    "guests": reservation.guests,
                    "reservation_date": reservation.reservation_date,
                    "reservation_time": reservation.reservation_time,
                    "id_table": reservation.id_table,
                    "status": reservation.status,
                    "notes": reservation.notes
                })
                return QueryResult(True, None)
        except Exception as e:
            return QueryResult(None, e)

    def update_reservation_status_db(self, reservation_id, status):
        try:
            with self.__engine.begin() as conn:
                query = text("""
                    UPDATE reservations
                    SET status = :status
                    WHERE id = :id
                """)
                conn.execute(query, {
                    "id": reservation_id,
                    "status": status
                })
                return QueryResult(True, None)
        except Exception as e:
            return QueryResult(None, e)

    def check_table_availability_db(self, table_id, date, time, exclude_reservation_id=None):
        try:
            with self.__engine.connect() as conn:
                # Check if there are any other reservations for this table at the same time
                if exclude_reservation_id:
                    query = text("""
                        SELECT COUNT(*) FROM reservations
                        WHERE id_table = :table_id
                        AND reservation_date = :date
                        AND reservation_time = :time
                        AND status IN (1, 2) -- Pending or confirmed
                        AND id != :exclude_id
                    """)
                    result = conn.execute(query, {
                        "table_id": table_id,
                        "date": date,
                        "time": time,
                        "exclude_id": exclude_reservation_id
                    }).scalar()
                else:
                    query = text("""
                        SELECT COUNT(*) FROM reservations
                        WHERE id_table = :table_id
                        AND reservation_date = :date
                        AND reservation_time = :time
                        AND status IN (1, 2) -- Pending or confirmed
                    """)
                    result = conn.execute(query, {
                        "table_id": table_id,
                        "date": date,
                        "time": time
                    }).scalar()

                # Also check if the table is occupied by an active order
                orders_query = text("""
                    SELECT COUNT(*) FROM orders
                    WHERE id_table = :table_id
                    AND order_date = :date
                    AND order_status < 4 -- Not closed
                """)
                orders_result = conn.execute(orders_query, {
                    "table_id": table_id,
                    "date": date
                }).scalar()

                # Table is available if there are no reservations or active orders
                is_available = (result == 0 and orders_result == 0)
                return QueryResult(is_available, None)
        except Exception as e:
            return QueryResult(None, e)
