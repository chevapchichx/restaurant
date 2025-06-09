from enum import IntEnum
from datetime import datetime


class ReservationStatus(IntEnum):
    PENDING = 1
    CONFIRMED = 2
    CANCELLED = 3
    COMPLETED = 4


class Reservation:
    def __init__(self, id_reservation=None, customer_name=None, phone_number=None,
                 guests=None, reservation_date=None, reservation_time=None,
                 id_table=None, status=None, notes=None):
        self.id_reservation = id_reservation
        self.customer_name = customer_name
        self.phone_number = phone_number
        self.guests = guests
        self.reservation_date = reservation_date
        self.reservation_time = reservation_time
        self.id_table = id_table
        self.__status = status if status is not None else ReservationStatus.PENDING
        self.notes = notes

    @property
    def status(self):
        return self.__status

    @property
    def status_name(self):
        if self.__status == ReservationStatus.PENDING:
            return "В ожидании"
        elif self.__status == ReservationStatus.CONFIRMED:
            return "Подтверждено"
        elif self.__status == ReservationStatus.CANCELLED:
            return "Отменено"
        elif self.__status == ReservationStatus.COMPLETED:
            return "Завершено"
        return "Неизвестно"

    @property
    def formatted_date(self):
        if isinstance(self.reservation_date, datetime):
            return self.reservation_date.strftime("%d.%m.%Y")
        return str(self.reservation_date)

    @property
    def formatted_time(self):
        if isinstance(self.reservation_time, datetime):
            return self.reservation_time.strftime("%H:%M")
        return str(self.reservation_time)
