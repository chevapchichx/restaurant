from PyQt6.QtWidgets import QMessageBox
from service.database_service import DatabaseService
from data.reservation_data import Reservation, ReservationStatus


class ReservationService:
    def get_reservations(self, date=None):
        data_service = DatabaseService()
        query = data_service.get_reservations_db(date)
        if query.error is None:
            result = query.result
            if result:
                reservations = [Reservation(
                    id_reservation=row[0],
                    customer_name=row[1],
                    phone_number=row[2],
                    guests=row[3],
                    reservation_date=row[4],
                    reservation_time=row[5],
                    id_table=row[6],
                    status=row[7],
                    notes=row[8]
                ) for row in result]
                return reservations
            return []
        else:
            QMessageBox.critical(
                None, "Ошибка", f"Ошибка подключения к базе данных: {query.error}")
            return None

    def add_reservation(self, reservation):
        data_service = DatabaseService()
        query = data_service.add_reservation_db(reservation)
        if query.error is None:
            return True
        else:
            QMessageBox.critical(
                None, "Ошибка", f"Ошибка подключения к базе данных: {query.error}")
            return False

    def update_reservation_status(self, reservation_id, status):
        data_service = DatabaseService()
        query = data_service.update_reservation_status_db(
            reservation_id, status)
        if query.error is None:
            return True
        else:
            QMessageBox.critical(
                None, "Ошибка", f"Ошибка подключения к базе данных: {query.error}")
            return False

    def check_table_availability(self, table_id, date, time, exclude_reservation_id=None):
        data_service = DatabaseService()
        query = data_service.check_table_availability_db(
            table_id, date, time, exclude_reservation_id)
        if query.error is None:
            return query.result
        else:
            QMessageBox.critical(
                None, "Ошибка", f"Ошибка подключения к базе данных: {query.error}")
            return False