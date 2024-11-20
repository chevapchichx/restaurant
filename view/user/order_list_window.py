from PyQt6.QtWidgets import (QApplication, QPushButton, QVBoxLayout, QHBoxLayout, QWidget, QLabel, QTableWidget, QTableWidgetItem)
from view.user.order_list_w_service import *

class Order_List_Window(QWidget):
    def __init__(self):
        super().__init__()
        self.user = User_Service().authorised_user
        self.UI_Order_List_Window()

    def UI_Order_List_Window(self):
        self.setWindowTitle("Текущие заказы")
        self.setGeometry(100, 100, 600, 450)
        self.setFixedSize(600, 450)

        main_layout = QVBoxLayout(self)

        top_layout = QHBoxLayout()
        self.add_order_button = QPushButton("Добавить заказ")
        self.info_button = QPushButton("Обо мне")
        self.exit_button = QPushButton("Выйти")

        top_layout.addWidget(self.add_order_button)
        top_layout.addStretch()
        self.user_name_label = QLabel(f"Официант: {self.user.first_name} {self.user.last_name}")
        top_layout.addWidget(self.user_name_label)
        top_layout.addStretch()
        top_layout.addWidget(self.info_button)

        self.orders_table = QTableWidget()
        self.orders_table.setColumnCount(5)
        self.orders_table.setHorizontalHeaderLabels(["Заказ", "Статус", "Стол", "Время", "Сумма"])
        self.orders_table.setRowCount(10)
        for i in range(10):
            self.orders_table.setItem(i, 0, QTableWidgetItem(f"{i+1}"))
            self.orders_table.setItem(i, 1, QTableWidgetItem("Готовится"))

        self.orders_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.orders_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)

        exit_layout = QHBoxLayout()
        exit_layout.addStretch()
        exit_layout.addWidget(self.exit_button)

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
#     auth_info = ["", "", "Официант", "Имя", "Фамилия"] 
#     window = WaiterOrderWindow(auth_info)
#     window.show()
#     sys.exit(app.exec())

