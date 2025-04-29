from PyQt6.QtWidgets import (
    QApplication, QPushButton, QVBoxLayout, QHBoxLayout,
    QWidget, QLabel, QTableWidget, QTableWidgetItem, QMessageBox
)
from PyQt6.QtCore import Qt
from view.order_list_w_service import *
from data.order_data import OrderStatus
from service.user_service import UserService, UserRole
from service.order_service import OrderService


class OrderListWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.user = UserService().authorised_user
        self.orders = OrderService().get_orders(self.user.id_staff, self.user.role)
        if self.orders is None:
            self.orders = []
        else:
            self.orders = sorted(
                self.orders, key=lambda order: order.full_date, reverse=True)
        self.ui_order_list_window()
        self.ui_update_order_list_table()

    def ui_order_list_window(self):
        self.setWindowTitle("Текущие заказы")
        self.setGeometry(400, 230, 680, 450)
        self.setFixedSize(680, 450)

        self.main_layout = QVBoxLayout(self)

        top_layout = QHBoxLayout()
        self.add_order_button = QPushButton("Новый заказ")
        self.add_order_button.setFixedSize(100, 25)
        self.add_order_button.setStyleSheet(
            "background-color: #7b99ca; font-size: 14px; color: white; border: 0; border-radius: 5px;")
        self.info_button = QPushButton("ЛК")
        self.info_button.setFixedSize(40, 25)
        self.info_button.setStyleSheet(
            "background-color: #7b99ca; font-size: 14px; color: white; border: 0; border-radius: 5px;")
        self.exit_button = QPushButton("Выйти")
        self.exit_button.setFixedSize(60, 25)
        self.exit_button.setStyleSheet(
            "background-color: #7b99ca; font-size: 14px; color: white; border: 0; border-radius: 5px;")

        top_layout.addWidget(self.add_order_button)
        top_layout.addStretch()
        self.user_name_label = QLabel(
            f"{self.user.role_name}: {self.user.first_name} {self.user.last_name}")
        top_layout.addWidget(self.user_name_label)
        top_layout.addStretch()

        self.staff_list = QPushButton("Управление персоналом")
        self.staff_list.setFixedSize(180, 25)
        self.staff_list.setStyleSheet(
            "background-color: #7b99ca; font-size: 14px; color: white; border: 0; border-radius: 5px;")

        if self.user.role == UserRole.ADMIN:
            top_layout.addWidget(self.staff_list)
            self.staff_list.clicked.connect(
                lambda: open_staff_list_window(self))

            self.stats_button = QPushButton("Статистика")
            self.stats_button.setFixedSize(100, 25)
            self.stats_button.setStyleSheet(
                "background-color: #7b99ca; font-size: 14px; color: white; border: 0; border-radius: 5px;")
            self.stats_button.clicked.connect(lambda: open_stats_window(self))
            top_layout.addWidget(self.stats_button)

        top_layout.addWidget(self.info_button)

        self.orders_table = QTableWidget()
        self.orders_table.setColumnCount(6)
        self.orders_table.setColumnWidth(0, 70)
        self.orders_table.setColumnWidth(1, 70)
        self.orders_table.setColumnWidth(2, 140)
        self.orders_table.setColumnWidth(3, 140)
        self.orders_table.setColumnWidth(4, 70)
        self.orders_table.setColumnWidth(5, 130)
        self.orders_table.setHorizontalHeaderLabels(
            ["Заказ", "Стол", "Время", "Дата", "Гости", "Статус"])
        self.orders_table.setSelectionBehavior(
            QTableWidget.SelectionBehavior.SelectRows)
        self.orders_table.setEditTriggers(
            QTableWidget.EditTrigger.NoEditTriggers)

        if self.user.role == UserRole.ADMIN:
            self.orders_table.setColumnCount(7)
            self.orders_table.setColumnWidth(0, 60)
            self.orders_table.setColumnWidth(1, 60)
            self.orders_table.setColumnWidth(2, 100)
            self.orders_table.setColumnWidth(3, 100)
            self.orders_table.setColumnWidth(4, 60)
            self.orders_table.setColumnWidth(5, 100)
            self.orders_table.setColumnWidth(6, 140)
            self.orders_table.setHorizontalHeaderLabels(
                ["Заказ", "Стол", "Время", "Дата", "Гости", "Статус", "Официант"])

        self.ui_update_order_list_table()

        exit_layout = QHBoxLayout()
        exit_layout.addStretch()
        exit_layout.addWidget(self.exit_button)

        self.main_layout.addLayout(top_layout)
        self.main_layout.addWidget(self.orders_table)
        self.main_layout.addLayout(exit_layout)

        self.add_order_button.clicked.connect(
            lambda: create_new_order(self, id_staff=self.user.id_staff))
        self.info_button.clicked.connect(lambda: open_user_info_window(self))
        self.exit_button.clicked.connect(lambda: open_auth_window(self))

        self.orders_table.cellDoubleClicked.connect(lambda: open_order_edit_window(
            self, id_order=self.filtered_orders[self.orders_table.currentRow()].id_order))

    def ui_update_order_list_table(self):
        self.filtered_orders = [
            order for order in self.orders if order.status != OrderStatus.CLOSED]
        unique_orders = {
            order.order_num: order for order in self.filtered_orders}

        self.orders_table.setRowCount(len(unique_orders))

        for i, order in enumerate(unique_orders.values()):
            item_order_num = QTableWidgetItem(f"{order.order_num}")
            item_order_num.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.orders_table.setItem(i, 0, item_order_num)

            item_table = QTableWidgetItem(f"{order.table}")
            item_table.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.orders_table.setItem(i, 1, item_table)

            item_time = QTableWidgetItem(f"{order.time}")
            item_time.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.orders_table.setItem(i, 2, item_time)

            item_date = QTableWidgetItem(f"{order.date}")
            item_date.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.orders_table.setItem(i, 3, item_date)

            item_guests = QTableWidgetItem(f"{order.guests}")
            item_guests.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.orders_table.setItem(i, 4, item_guests)

            item_status = QTableWidgetItem(f"{order.status_name}")
            item_status.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.orders_table.setItem(i, 5, item_status)

            item_staff = QTableWidgetItem(
                f"{order.staff.first_name} {order.staff.last_name}")
            item_staff.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.orders_table.setItem(i, 6, item_staff)
