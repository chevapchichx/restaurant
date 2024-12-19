from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (QApplication, QHBoxLayout, QLabel, QMessageBox,
                            QPushButton, QTableWidget, QTableWidgetItem,
                            QVBoxLayout, QWidget)

from service.dish_service import *
from service.order_service import *
from service.user_service import UserRole, UserService
from view.dish_list_w_service import *


class DishListWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.user = UserService().authorised_user
        self.order_items = OrderService().get_order_items()
        if self.order_items is None:
            self.order_items = []
        self.ui_dish_list_window()
    
    def ui_dish_list_window(self):
        self.setWindowTitle("Текущие блюда")
        self.setGeometry(400, 230, 650, 450)
        self.setFixedSize(680, 450)

        self.main_layout = QVBoxLayout(self)

        top_layout = QHBoxLayout()
        self.info_button = QPushButton("ЛК")
        self.info_button.setFixedSize(40, 25)
        self.info_button.setStyleSheet("background-color: #7b99ca; font-size: 14px; color: white; border: 0; border-radius: 5px;")

        self.exit_button = QPushButton("Выйти")
        self.exit_button.setFixedSize(60, 25)
        self.exit_button.setStyleSheet("background-color: #7b99ca; font-size: 14px; color: white; border: 0; border-radius: 5px;")

        top_layout.addStretch()
        self.user_name_label = QLabel(f"{self.user.role_name}: {self.user.first_name} {self.user.last_name}")
        top_layout.addWidget(self.user_name_label)
        top_layout.addStretch()
        top_layout.addWidget(self.info_button)

        self.dish_table = QTableWidget()
        self.dish_table.setColumnCount(5)
        self.dish_table.setColumnWidth(0, 250)  #220
        self.dish_table.setColumnWidth(1, 80)  #60
        self.dish_table.setColumnWidth(2, 80)  #80 
        self.dish_table.setColumnWidth(3, 90)  #80
        self.dish_table.setColumnWidth(4, 120)  #110
        self.dish_table.setHorizontalHeaderLabels(["Блюдо", "Вес", "Количество", "Время", ""])
        self.dish_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.dish_table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)

        self.ui_update_dish_list_table()

        exit_layout = QHBoxLayout()
        exit_layout.addStretch()
        exit_layout.addWidget(self.exit_button)

        self.main_layout.addLayout(top_layout)
        self.main_layout.addWidget(self.dish_table)
        self.main_layout.addLayout(exit_layout)

        self.info_button.clicked.connect(lambda: open_user_info_window(self))
        self.exit_button.clicked.connect(lambda: open_auth_window(self))

    def ui_update_dish_list_table(self):
        filtered_order_items = [order_item for order_item in self.order_items if order_item.status == DishStatus.COOKING]
        filtered_order_items = sorted(filtered_order_items, key=lambda item: item.added_time)

        self.dish_table.setRowCount(len(filtered_order_items))

        for i, order_item in enumerate(filtered_order_items):       
            item_dish_name = QTableWidgetItem(order_item.dish.dish_name)
            item_dish_name.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.dish_table.setItem(i, 0, item_dish_name)
            
            item_dish_weight = QTableWidgetItem(str(order_item.dish.weight))
            item_dish_weight.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.dish_table.setItem(i, 1, item_dish_weight)
            
            item_amount = QTableWidgetItem(str(order_item.amount))
            item_amount.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.dish_table.setItem(i, 2, item_amount)

            item_dish_time = QTableWidgetItem(order_item.added_time.strftime("%H:%M:%S"))
            item_dish_time.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.dish_table.setItem(i, 3, item_dish_time)
            
            if order_item.status == DishStatus.COOKING:
                update_button = QPushButton("Приготовлено")
                update_button.clicked.connect(lambda _, order_item=order_item: update_item_order_status(self, order_item))
                self.dish_table.setCellWidget(i, 4, update_button)