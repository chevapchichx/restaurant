from PyQt6.QtWidgets import (
    QApplication, QPushButton, QVBoxLayout, QHBoxLayout,
    QWidget, QLabel, QTableWidget, QTableWidgetItem, QDateEdit,
    QMessageBox
)
from PyQt6.QtCore import Qt, QDate
from service.reservation_service import ReservationService
from service.user_service import UserService, UserRole
from data.reservation_data import ReservationStatus
from view.reservation_list_w_service import *


class ReservationListWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.user = UserService().authorised_user
        self.reservation_service = ReservationService()
        self.ui_reservation_list_window()

    def ui_reservation_list_window(self):
        self.setWindowTitle("Управление бронированием")
        self.setGeometry(400, 230, 650, 450)
        self.setFixedSize(680, 450)

        main_layout = QVBoxLayout(self)

        top_layout = QHBoxLayout()

        self.date_label = QLabel("Дата:")
        self.date_edit = QDateEdit()
        self.date_edit.setDate(QDate.currentDate())
        self.date_edit.setCalendarPopup(True)
        self.date_edit.dateChanged.connect(self.update_reservations_table)

        self.add_reservation_button = QPushButton("Добавить бронирование")
        self.add_reservation_button.setFixedSize(180, 25)
        self.add_reservation_button.setStyleSheet(
            "background-color: #7b99ca; font-size: 14px; color: white; border: 0; border-radius: 5px;")
        self.add_reservation_button.clicked.connect(
            lambda: open_add_reservation_window(self))

        self.back_button = QPushButton("Назад")
        self.back_button.setFixedSize(60, 25)
        self.back_button.setStyleSheet(
            "background-color: #7b99ca; font-size: 14px; color: white; border: 0; border-radius: 5px;")
        self.back_button.clicked.connect(lambda: open_order_list_window(self))

        top_layout.addWidget(self.date_label)
        top_layout.addWidget(self.date_edit)
        top_layout.addStretch()
        top_layout.addWidget(self.add_reservation_button)
        top_layout.addWidget(self.back_button)

        main_layout.addLayout(top_layout)

        self.reservations_table = QTableWidget()
        self.reservations_table.setColumnCount(7)
        self.reservations_table.setColumnWidth(0, 130)  
        self.reservations_table.setColumnWidth(1, 105)  
        self.reservations_table.setColumnWidth(2, 50)  
        self.reservations_table.setColumnWidth(3, 50)   
        self.reservations_table.setColumnWidth(4, 90) 
        self.reservations_table.setColumnWidth(5, 85)   
        self.reservations_table.setColumnWidth(6, 130) 

        self.reservations_table.setHorizontalHeaderLabels(
            ["Имя клиента", "Телефон", "Гости", "Стол", "Время", "Статус", "Действия"])
        self.reservations_table.setSelectionBehavior(
            QTableWidget.SelectionBehavior.SelectRows)
        self.reservations_table.setEditTriggers(
            QTableWidget.EditTrigger.NoEditTriggers)

        main_layout.addWidget(self.reservations_table)

        self.update_reservations_table()
        self.setLayout(main_layout)

    def update_reservations_table(self):
        selected_date = self.date_edit.date().toString("yyyy-MM-dd")
        reservations = self.reservation_service.get_reservations(selected_date)

        self.reservations_table.setRowCount(0)
        if not reservations:
            return

        self.reservations_table.setRowCount(len(reservations))

        for i, reservation in enumerate(reservations):
            name_item = QTableWidgetItem(reservation.customer_name)
            name_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.reservations_table.setItem(i, 0, name_item)

            phone_item = QTableWidgetItem(reservation.phone_number)
            phone_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.reservations_table.setItem(i, 1, phone_item)

            guests_item = QTableWidgetItem(str(reservation.guests))
            guests_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.reservations_table.setItem(i, 2, guests_item)

            table_item = QTableWidgetItem(str(reservation.id_table))
            table_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.reservations_table.setItem(i, 3, table_item)

            time_str = reservation.formatted_time
            if len(time_str) > 5: 
                time_str = time_str[:5]  

            time_item = QTableWidgetItem(time_str)
            time_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.reservations_table.setItem(i, 4, time_item)

            status_item = QTableWidgetItem(reservation.status_name)
            status_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.reservations_table.setItem(i, 5, status_item)

            actions_layout = QHBoxLayout()
            actions_layout.setContentsMargins(5, 0, 5, 0)

            if reservation.status == ReservationStatus.PENDING:
                confirm_button = QPushButton("✓")
                confirm_button.setFixedSize(25, 25)
                confirm_button.setStyleSheet(
                    "background-color: #4CAF50; color: white;")
                confirm_button.clicked.connect(
                    lambda _, r_id=reservation.id_reservation: self.confirm_reservation(r_id))
                actions_layout.addWidget(confirm_button)

                cancel_button = QPushButton("✗")
                cancel_button.setFixedSize(25, 25)
                cancel_button.setStyleSheet(
                    "background-color: #F44336; color: white;")
                cancel_button.clicked.connect(
                    lambda _, r_id=reservation.id_reservation: self.cancel_reservation(r_id))
                actions_layout.addWidget(cancel_button)

            elif reservation.status == ReservationStatus.CONFIRMED:
                complete_button = QPushButton("Завершить")
                complete_button.setFixedSize(70, 25)
                complete_button.setStyleSheet(
                    "background-color: #558dbb; color: white;")
                complete_button.clicked.connect(
                    lambda _, r_id=reservation.id_reservation: self.complete_reservation(r_id))
                actions_layout.addWidget(complete_button)

                cancel_button = QPushButton("✗")
                cancel_button.setFixedSize(25, 25)
                cancel_button.setStyleSheet(
                    "background-color: #F44336; color: white;")
                cancel_button.clicked.connect(
                    lambda _, r_id=reservation.id_reservation: self.cancel_reservation(r_id))
                actions_layout.addWidget(cancel_button)

            actions_widget = QWidget()
            actions_widget.setLayout(actions_layout)
            self.reservations_table.setCellWidget(i, 6, actions_widget)

    def confirm_reservation(self, reservation_id):
        if self.reservation_service.update_reservation_status(reservation_id, ReservationStatus.CONFIRMED):
            self.update_reservations_table()

    def cancel_reservation(self, reservation_id):
        msg = QMessageBox(self)
        msg.setWindowTitle("Подтверждение")
        msg.setText("Вы уверены, что хотите отменить это бронирование?")
        msg.setStandardButtons(
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        yes_button = msg.button(QMessageBox.StandardButton.Yes)
        no_button = msg.button(QMessageBox.StandardButton.No)
        yes_button.setText("Да")
        no_button.setText("Нет")
        result = msg.exec()

        if result == QMessageBox.StandardButton.Yes:
            if self.reservation_service.update_reservation_status(reservation_id, ReservationStatus.CANCELLED):
                self.update_reservations_table()

    def complete_reservation(self, reservation_id):
        if self.reservation_service.update_reservation_status(reservation_id, ReservationStatus.COMPLETED):
            self.update_reservations_table()