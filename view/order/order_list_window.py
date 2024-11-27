
from PyQt6.QtWidgets import (QApplication, QPushButton, QVBoxLayout, QHBoxLayout, QWidget, QLabel, QTableWidget, QTableWidgetItem)
from PyQt6.QtCore import Qt
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from view.order.order_list_w_service import *
from view.order.order_edit_w_service import *
from service.user_service import *
from service.order_service import *

class Order_List_Window(QWidget):
    def __init__(self):
        super().__init__()
        self.user = User_Service().authorised_user
        self.orders = sorted(Order_Service().get_orders(self.user.id_worker, self.user.role), key=lambda order: order.date, reverse=True)
        self.UI_Order_List_Window()

    def UI_Order_List_Window(self):
        self.setWindowTitle("Текущие заказы")
        self.setGeometry(400, 230, 650, 450)
        self.setFixedSize(650, 450)

        main_layout = QVBoxLayout(self)

        top_layout = QHBoxLayout()
        self.add_order_button = QPushButton("Новый заказ")
        self.info_button = QPushButton("Кабинет")
        self.exit_button = QPushButton("Выйти")
        self.button_1 = QPushButton("Для админа")

        top_layout.addWidget(self.add_order_button)
        top_layout.addStretch()
        self.user_name_label = QLabel(f"{self.user.role_name}: {self.user.first_name} {self.user.last_name}")
        top_layout.addWidget(self.user_name_label)
        top_layout.addStretch()
        top_layout.addWidget(self.info_button)

        self.orders_table = QTableWidget()
        self.orders_table.setColumnCount(6)
        self.orders_table.setColumnWidth(0, 80)
        self.orders_table.setHorizontalHeaderLabels(["Заказ", "Стол", "Время", "Дата", "Гости", "Статус"])

        filtered_orders = [order for order in self.orders if order.status != Order_Status.CLOSED]
        unique_orders = {order.order_num: order for order in filtered_orders}

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

            if self.user.role == User_Role.ADMIN:
                self.orders_table.setColumnCount(7)
                self.orders_table.setColumnWidth(0, 60)
                self.orders_table.setColumnWidth(1, 60)
                self.orders_table.setColumnWidth(2, 90)
                self.orders_table.setColumnWidth(3, 95)
                self.orders_table.setColumnWidth(4, 60)
                self.orders_table.setColumnWidth(5, 100)
                self.orders_table.setColumnWidth(6, 120)
                self.orders_table.setHorizontalHeaderLabels(["Заказ", "Стол", "Время", "Дата", "Гости", "Статус", "Официант"])
                item_worker = QTableWidgetItem(f"{order.worker.first_name} {order.worker.last_name}")
                item_worker.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.orders_table.setItem(i, 6, item_worker)

        self.orders_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.orders_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)

        self.orders_table.cellDoubleClicked.connect(lambda: open_order_edit_window(self, id_order=filtered_orders[self.orders_table.currentRow()].id_order))

        exit_layout = QHBoxLayout()
        exit_layout.addStretch()
        exit_layout.addWidget(self.exit_button)

        if self.user.role == User_Role.ADMIN:
            exit_layout.addWidget(self.button_1)

        main_layout.addLayout(top_layout)
        main_layout.addWidget(self.orders_table)
        main_layout.addLayout(exit_layout)

        self.add_order_button.clicked.connect(self.open_manage_orders_window)
        self.info_button.clicked.connect(lambda: open_user_info_window(self))
        self.exit_button.clicked.connect(lambda: open_auth_window(self))

    def open_manage_orders_window(self):
        print("Открытие окна управления заказами")

# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     window = Order_List_Window()
#     window.show()
#     sys.exit(app.exec())

