from PyQt6.QtWidgets import (
    QApplication, QPushButton, QVBoxLayout, QHBoxLayout,
    QWidget, QLabel, QLineEdit, QDateEdit, QTimeEdit,
    QSpinBox, QComboBox, QTextEdit, QMessageBox
)
from PyQt6.QtCore import Qt, QDate, QTime
from service.reservation_service import ReservationService
from service.order_service import OrderService
from data.reservation_data import Reservation, ReservationStatus
from view.add_reservation_w_service import *


class AddReservationWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.reservation_service = ReservationService()
        self.order_service = OrderService()
        self.ui_add_reservation_window()

    def ui_add_reservation_window(self):
        self.setWindowTitle("Добавление бронирования")
        self.setGeometry(400, 230, 650, 450)
        self.setFixedSize(680, 450)

        main_layout = QVBoxLayout(self)

        form_layout = QVBoxLayout()

        name_layout = QHBoxLayout()
        self.name_label = QLabel("Имя клиента:")
        self.name_label.setFixedWidth(120)
        self.name_input = QLineEdit()
        name_layout.addWidget(self.name_label)
        name_layout.addWidget(self.name_input)
        form_layout.addLayout(name_layout)

        phone_layout = QHBoxLayout()
        self.phone_label = QLabel("Телефон:")
        self.phone_label.setFixedWidth(120)
        self.phone_input = QLineEdit()
        self.phone_input.setPlaceholderText("+7XXXXXXXXXX")
        phone_layout.addWidget(self.phone_label)
        phone_layout.addWidget(self.phone_input)
        form_layout.addLayout(phone_layout)

        datetime_layout = QHBoxLayout()

        self.date_label = QLabel("Дата:")
        self.date_label.setFixedWidth(120)
        self.date_edit = QDateEdit()
        self.date_edit.setDate(QDate.currentDate())
        self.date_edit.setCalendarPopup(True)
        self.date_edit.setMinimumDate(QDate.currentDate())
        self.date_edit.dateChanged.connect(self.check_table_availability)
        datetime_layout.addWidget(self.date_label)
        datetime_layout.addWidget(self.date_edit)

        self.time_label = QLabel("Время:")
        self.time_edit = QTimeEdit()
        self.time_edit.setTime(QTime.currentTime())
        self.time_edit.setDisplayFormat("HH:mm")
        self.time_edit.timeChanged.connect(self.check_table_availability)
        datetime_layout.addWidget(self.time_label)
        datetime_layout.addWidget(self.time_edit)

        form_layout.addLayout(datetime_layout)

        guests_table_layout = QHBoxLayout()

        self.guests_label = QLabel("Количество гостей:")
        self.guests_label.setFixedWidth(120)
        self.guests_spinbox = QSpinBox()
        self.guests_spinbox.setMinimum(1)
        self.guests_spinbox.setMaximum(20)
        self.guests_spinbox.valueChanged.connect(self.update_available_tables)
        guests_table_layout.addWidget(self.guests_label)
        guests_table_layout.addWidget(self.guests_spinbox)

        self.table_label = QLabel("Стол:")
        self.table_combobox = QComboBox()
        self.table_combobox.currentIndexChanged.connect(
            self.check_table_availability)
        guests_table_layout.addWidget(self.table_label)
        guests_table_layout.addWidget(self.table_combobox)

        form_layout.addLayout(guests_table_layout)

        notes_layout = QHBoxLayout()
        self.notes_label = QLabel("Примечания:")
        self.notes_label.setFixedWidth(120)
        self.notes_text = QTextEdit()
        self.notes_text.setMaximumHeight(100)
        notes_layout.addWidget(self.notes_label)
        notes_layout.addWidget(self.notes_text)
        form_layout.addLayout(notes_layout)

        status_layout = QHBoxLayout()
        self.status_label = QLabel("Статус:")
        self.status_label.setFixedWidth(120)
        self.availability_label = QLabel("Проверьте доступность стола")
        self.availability_label.setStyleSheet("color: gray;")
        status_layout.addWidget(self.status_label)
        status_layout.addWidget(self.availability_label)
        form_layout.addLayout(status_layout)

        main_layout.addLayout(form_layout)

        buttons_layout = QHBoxLayout()
        buttons_layout.addStretch()

        self.save_button = QPushButton("Сохранить")
        self.save_button.setFixedSize(100, 25)
        self.save_button.setStyleSheet(
            "background-color: #7b99ca; font-size: 14px; color: white; border: 0; border-radius: 5px;")
        self.save_button.clicked.connect(self.save_reservation)
        self.save_button.setEnabled(False)

        self.cancel_button = QPushButton("Назад")
        self.cancel_button.setFixedSize(100, 25)
        self.cancel_button.setStyleSheet(
            "background-color: #7b99ca; font-size: 14px; color: white; border: 0; border-radius: 5px;")
        self.cancel_button.clicked.connect(
            lambda: open_reservation_list_window(self))

        buttons_layout.addWidget(self.save_button)
        buttons_layout.addWidget(self.cancel_button)

        main_layout.addLayout(buttons_layout)

        self.setLayout(main_layout)

        self.update_available_tables()

    def update_available_tables(self):
        guests = self.guests_spinbox.value()
        self.table_combobox.clear()


        tables = [1, 2, 3, 4, 5, 6]  
        capacities = {1: 4, 2: 4, 3: 4, 4: 2, 5: 6, 6: 6}

        for table_id in tables:
            if capacities.get(table_id, 0) >= guests:
                self.table_combobox.addItem(
                    f"Стол {table_id} (мест: {capacities[table_id]})", table_id)

        if self.table_combobox.count() > 0:
            self.check_table_availability()
        else:
            self.availability_label.setText(
                "Нет столов с достаточным количеством мест")
            self.availability_label.setStyleSheet("color: red;")
            self.save_button.setEnabled(False)

    def check_table_availability(self):
        if self.table_combobox.count() == 0:
            return

        table_id = self.table_combobox.currentData()
        date = self.date_edit.date().toString("yyyy-MM-dd")
        time = self.time_edit.time().toString("HH:mm:ss")

        is_available = self.reservation_service.check_table_availability(
            table_id, date, time)

        if is_available:
            self.availability_label.setText("Стол доступен")
            self.availability_label.setStyleSheet("color: green;")
            self.save_button.setEnabled(True)
        else:
            self.availability_label.setText("Стол занят в это время")
            self.availability_label.setStyleSheet("color: red;")
            self.save_button.setEnabled(False)

    def save_reservation(self):
        if not self.name_input.text():
            QMessageBox.warning(self, "Предупреждение",
                                "Пожалуйста, введите имя клиента")
            return

        if not self.phone_input.text():
            QMessageBox.warning(self, "Предупреждение",
                                "Пожалуйста, введите номер телефона")
            return

        # Create a new reservation
        reservation = Reservation(
            customer_name=self.name_input.text(),
            phone_number=self.phone_input.text(),
            guests=self.guests_spinbox.value(),
            reservation_date=self.date_edit.date().toString("yyyy-MM-dd"),
            reservation_time=self.time_edit.time().toString("HH:mm:ss"),
            id_table=self.table_combobox.currentData(),
            status=ReservationStatus.PENDING,
            notes=self.notes_text.toPlainText()
        )

        if self.reservation_service.add_reservation(reservation):
            QMessageBox.information(
                self, "Успех", "Бронирование успешно добавлено")
            open_reservation_list_window(self)
        else:
            QMessageBox.critical(
                self, "Ошибка", "Не удалось добавить бронирование")
