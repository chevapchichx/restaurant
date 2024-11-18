from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QVBoxLayout, QHBoxLayout, 
    QWidget, QLabel, QTableWidget, QTableWidgetItem
)
from PyQt6.QtCore import Qt
import sys
from auth_service import *

class WaiterWindow(QWidget):
    def __init__(self, auth_info):
        super().__init__()
        self.auth_info = auth_info
        self.UI_WaiterWindow()

    def UI_WaiterWindow(self):
        self.setWindowTitle("Управление рестораном")
        self.setGeometry(100, 100, 600, 450)

        main_layout = QVBoxLayout(self)

        top_layout = QHBoxLayout()
        self.manage_orders_button = QPushButton("Управление заказами")
        self.about_button = QPushButton("Обо мне")
        self.exit_button = QPushButton("ВЫХОД")

        top_layout.addWidget(self.manage_orders_button)
        top_layout.addStretch()
        self.user_name_label = QLabel(f"Официант: {self.auth_info[3]} {self.auth_info[4]}")
        top_layout.addWidget(self.user_name_label)
        top_layout.addStretch()
        top_layout.addWidget(self.about_button)

        self.orders_table = QTableWidget()
        self.orders_table.setColumnCount(2)
        self.orders_table.setHorizontalHeaderLabels(["Заказ", "Статус"])
        self.orders_table.setRowCount(5)
        for i in range(5):
            self.orders_table.setItem(i, 0, QTableWidgetItem(f"Блюдо {i+1}"))
            self.orders_table.setItem(i, 1, QTableWidgetItem("Готовится"))

        self.orders_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.orders_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)

        exit_layout = QHBoxLayout()
        exit_layout.addStretch()
        exit_layout.addWidget(self.exit_button)

        main_layout.addLayout(top_layout)
        main_layout.addWidget(self.orders_table)
        main_layout.addLayout(exit_layout)

        self.manage_orders_button.clicked.connect(self.open_manage_orders_window)
        self.about_button.clicked.connect(self.open_about_window)
        self.exit_button.clicked.connect(lambda: open_auth_window(self))

    def open_manage_orders_window(self):
        print("Открытие окна управления заказами")

    def open_about_window(self):
        print("Открытие окна 'Обо мне'")




# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     auth_info = ["", "", "Официант", "Имя", "Фамилия"] 
#     window = WaiterWindow(auth_info)
#     window.show()
#     sys.exit(app.exec())

