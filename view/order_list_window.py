from PyQt6.QtWidgets import (
    QApplication, QPushButton, QVBoxLayout, QHBoxLayout,
    QWidget, QLabel, QTableWidget, QTableWidgetItem, QMessageBox,
    QLineEdit, QComboBox
)
from PyQt6.QtCore import Qt
from view.order_list_w_service import *
from data.order_data import OrderStatus
from service.user_service import UserService, UserRole
from service.order_service import OrderService
from PyQt6.QtGui import QColor, QIcon


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
        self.search_text = ""
        self.search_field = "all"
        self.ui_order_list_window()
        self.ui_update_order_list_table()

    def ui_order_list_window(self):
        self.setWindowTitle("Текущие заказы")
        self.setWindowIcon(QIcon("restaurant_icon.ico"))
        # self.setGeometry(400, 230, 680, 450)
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

        self.exit_layout = QHBoxLayout()

        if self.user.role == UserRole.ADMIN:
            self.exit_layout.addWidget(self.staff_list)
            self.staff_list.clicked.connect(
                lambda: open_staff_list_window(self))

            self.menu_button = QPushButton("Управление меню")
            self.menu_button.setFixedSize(150, 25)
            self.menu_button.setStyleSheet(
                "background-color: #7b99ca; font-size: 14px; color: white; border: 0; border-radius: 5px;")
            self.menu_button.clicked.connect(
                lambda: open_menu_management_window(self))
            self.exit_layout.addWidget(self.menu_button)

            self.stats_button = QPushButton("Статистика")
            self.stats_button.setFixedSize(100, 25)
            self.stats_button.setStyleSheet(
                "background-color: #7b99ca; font-size: 14px; color: white; border: 0; border-radius: 5px;")
            self.stats_button.clicked.connect(lambda: open_stats_window(self))
            self.exit_layout.addWidget(self.stats_button)

        if self.user.role == UserRole.ADMIN or self.user.role == UserRole.WAITER:
            self.reservation_button = QPushButton("Бронирование")
            self.reservation_button.setFixedSize(120, 25)
            self.reservation_button.setStyleSheet(
                "background-color: #7b99ca; font-size: 14px; color: white; border: 0; border-radius: 5px;")
            self.reservation_button.clicked.connect(
                lambda: open_reservation_list_window(self))
            top_layout.addWidget(self.reservation_button)

        top_layout.addWidget(self.info_button)

        search_layout = QHBoxLayout()
        search_label = QLabel("Поиск:")
        search_label.setFixedWidth(50)

        self.search_field_combo = QComboBox()
        self.search_field_combo.addItems(["Номер заказа", "Номер стола"])
        self.search_field_combo.setFixedWidth(150)
        self.search_field_combo.currentTextChanged.connect(
            self.update_search_field)

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Введите текст для поиска")
        self.search_input.textChanged.connect(self.on_search_text_changed)

        search_layout.addWidget(search_label)
        search_layout.addWidget(self.search_field_combo)
        search_layout.addWidget(self.search_input)

        self.orders_table = QTableWidget()
        self.orders_table.setColumnCount(6)
        self.orders_table.setColumnWidth(0, 70)
        self.orders_table.setColumnWidth(1, 70)
        self.orders_table.setColumnWidth(2, 140)
        self.orders_table.setColumnWidth(3, 140)
        self.orders_table.setColumnWidth(4, 70)
        self.orders_table.setColumnWidth(5, 150)
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
            self.orders_table.setColumnWidth(5, 110)
            self.orders_table.setColumnWidth(6, 150)
            self.orders_table.setHorizontalHeaderLabels(
                ["Заказ", "Стол", "Время", "Дата", "Гости", "Статус", "Официант"])

        self.ui_update_order_list_table()

        self.exit_layout.addStretch()
        self.exit_layout.addWidget(self.exit_button)

        self.main_layout.addLayout(top_layout)
        self.main_layout.addLayout(search_layout)
        self.main_layout.addWidget(self.orders_table)
        self.main_layout.addLayout(self.exit_layout)

        self.add_order_button.clicked.connect(
            lambda: create_new_order(self, id_staff=self.user.id_staff))
        self.info_button.clicked.connect(lambda: open_user_info_window(self))
        self.exit_button.clicked.connect(lambda: open_auth_window(self))

        self.orders_table.cellDoubleClicked.connect(lambda: open_order_edit_window(
            self, id_order=self.filtered_orders[self.orders_table.currentRow()].id_order))

    def update_search_field(self, text):

        if text == "Номер заказа":
            self.search_field = "order_num"
        elif text == "Номер стола":
            self.search_field = "table"

        self.filter_orders()

    def on_search_text_changed(self, text):
        self.search_text = text
        self.filter_orders()

    def filter_orders(self):
        if not self.search_text:
            self.ui_update_order_list_table()
            return

        self.filtered_orders = []
        search_text = self.search_text.lower()

        for order in self.orders:
            if order.status == OrderStatus.CLOSED:
                continue

            if self.search_field == "order_num" and str(order.order_num).lower().find(search_text) != -1:
                self.filtered_orders.append(order)
            elif self.search_field == "table" and str(order.table).lower().find(search_text) != -1:
                self.filtered_orders.append(order)

        self.update_table()

    def ui_update_order_list_table(self):
        self.filtered_orders = [
            order for order in self.orders if order.status != OrderStatus.CLOSED]
        self.update_table()

    def update_table(self):
        unique_orders = {
            order.order_num: order for order in self.filtered_orders}

        self.orders_table.setRowCount(len(unique_orders))

        highlight_color = "#4D9ADB"
        use_highlight = len(self.search_text) > 0

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

            if self.user.role == UserRole.ADMIN:
                item_staff = QTableWidgetItem(
                    f"{order.staff.first_name} {order.staff.last_name}")
                item_staff.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.orders_table.setItem(i, 6, item_staff)

            if use_highlight:
                search_text = self.search_text.lower()
                if self.search_field == "order_num" and str(order.order_num).lower().find(search_text) != -1:
                    self.highlight_row(i, highlight_color)
                elif self.search_field == "table" and str(order.table).lower().find(search_text) != -1:
                    self.highlight_row(i, highlight_color)

    def highlight_row(self, row, color):
        for col in range(self.orders_table.columnCount()):
            item = self.orders_table.item(row, col)
            if item:
                item.setBackground(QColor(color))
