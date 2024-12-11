from PyQt6.QtWidgets import (
    QApplication, QPushButton, QVBoxLayout, QHBoxLayout, 
    QWidget, QLabel, QTableWidget, QTableWidgetItem
)
from PyQt6.QtCore import Qt
from view.order_list_w_service import *
from data.order_data import OrderStatus
from service.user_service import UserService
from service.order_service import OrderService

class OrderListWindow(QWidget): 
    def __init__(self):
        super().__init__()
        self.user = UserService().authorised_user
        self.orders = OrderService().get_orders(self.user.id_staff, self.user.role)
        if self.orders is None:
            self.orders = []
        else:
            self.orders = sorted(self.orders, key=lambda order: order.full_date, reverse=True)
        self.ui_order_list_window()  

    def ui_order_list_window(self): 
        self.setWindowTitle("Текущие заказы")
        self.setGeometry(400, 230, 650, 450)
        self.setFixedSize(680, 450)

        main_layout = QVBoxLayout(self)

        top_layout = QHBoxLayout()
        self.add_order_button = QPushButton("Новый заказ")
        self.info_button = QPushButton("Кабинет")
        self.exit_button = QPushButton("Выйти")

        top_layout.addWidget(self.add_order_button)
        top_layout.addStretch()
        self.user_name_label = QLabel(f"{self.user.role_name}: {self.user.first_name} {self.user.last_name}")
        top_layout.addWidget(self.user_name_label)
        top_layout.addStretch()

        self.staff_list = QPushButton("Управление персоналом")

        if self.user.role == UserRole.ADMIN:
            top_layout.addWidget(self.staff_list)
            self.staff_list.clicked.connect(lambda: open_staff_list_window(self))

        top_layout.addWidget(self.info_button)

        self.orders_table = QTableWidget()
        self.orders_table.setColumnCount(6)
        self.orders_table.setColumnWidth(0, 80)
        self.orders_table.setHorizontalHeaderLabels(["Заказ", "Стол", "Время", "Дата", "Гости", "Статус"])

        filtered_orders = [order for order in self.orders if order.status != OrderStatus.CLOSED]
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

            if self.user.role == UserRole.ADMIN:
                self.orders_table.setColumnCount(7)
                self.orders_table.setColumnWidth(0, 60)
                self.orders_table.setColumnWidth(1, 60)
                self.orders_table.setColumnWidth(2, 90)
                self.orders_table.setColumnWidth(3, 95)
                self.orders_table.setColumnWidth(4, 60)
                self.orders_table.setColumnWidth(5, 100)
                self.orders_table.setColumnWidth(6, 120)
                self.orders_table.setHorizontalHeaderLabels(["Заказ", "Стол", "Время", "Дата", "Гости", "Статус", "Официант"])
                item_staff = QTableWidgetItem(f"{order.staff.first_name} {order.staff.last_name}")
                item_staff.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.orders_table.setItem(i, 6, item_staff)

        self.orders_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.orders_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)

        self.orders_table.cellDoubleClicked.connect(lambda: open_order_edit_window(self, id_order=filtered_orders[self.orders_table.currentRow()].id_order))

        exit_layout = QHBoxLayout()
        exit_layout.addStretch()
        exit_layout.addWidget(self.exit_button)

        main_layout.addLayout(top_layout)
        main_layout.addWidget(self.orders_table)
        main_layout.addLayout(exit_layout)

        self.add_order_button.clicked.connect(lambda: create_new_order(self, id_staff=self.user.id_staff))
        self.info_button.clicked.connect(lambda: open_user_info_window(self))
        self.exit_button.clicked.connect(lambda: open_auth_window(self))


# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     window = Order_List_Window()
#     window.show()
#     sys.exit(app.exec())

