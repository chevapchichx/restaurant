from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (QApplication, QGridLayout, QHBoxLayout,
                            QLabel, QPushButton, QVBoxLayout, QWidget)

from service.order_service import OrderService
from view.order_create_w_service import *


class OrderCreateWindow(QWidget):
    def __init__(self, id_order, order_num):
        super().__init__()
        self.order_service = OrderService()
        self.selected_table = None
        self.selected_guests = 0
        self.id_order = id_order
        self.order_num = order_num
        self.ui_order_create_window()

    def ui_order_create_window(self):
        self.setWindowTitle(f"Новый заказ {self.order_num}")
        self.setGeometry(400, 230, 650, 450)
        self.setFixedSize(650, 450)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)

        table_layout = QVBoxLayout()
        table_layout.setSpacing(10)

        self.table_number_label = QLabel("Выберите стол")
        self.table_number_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        table_layout.addWidget(self.table_number_label)

        self.table_number_layout = QGridLayout()
        self.table_number_buttons = []
        for i in range(6):
            button = QPushButton(str(i + 1))
            button.setFixedSize(50, 50)
            if self.order_service.get_is_table_occupied(int(button.text())):
                button.setEnabled(False)
            else:
                button.clicked.connect(lambda _, b=button: update_table_button(self, b))
            self.table_number_buttons.append(button)
            self.table_number_layout.addWidget(button, 0, i, alignment=Qt.AlignmentFlag.AlignCenter)
        table_layout.addLayout(self.table_number_layout)

        self.table_button = QLabel("Стол: не выбран")
        self.table_button.setAlignment(Qt.AlignmentFlag.AlignCenter)
        table_layout.addWidget(self.table_button)

        guest_layout = QVBoxLayout()
        guest_layout.setSpacing(10)

        self.guests_number_label = QLabel("Выберите количество гостей")
        self.guests_number_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        guest_layout.addWidget(self.guests_number_label)

        self.guests_number_layout = QGridLayout()
        self.guests_number_buttons = []
        for i in range(6):
            button = QPushButton(str(i + 1))
            button.setFixedSize(50, 50)
            button.clicked.connect(lambda _, b=button: update_guests_button(self, b))
            self.guests_number_buttons.append(button)
            self.guests_number_layout.addWidget(button, 0, i, alignment=Qt.AlignmentFlag.AlignCenter)
        guest_layout.addLayout(self.guests_number_layout)

        self.guests_button = QLabel("Количество гостей: не выбрано")
        self.guests_button.setAlignment(Qt.AlignmentFlag.AlignCenter)
        guest_layout.addWidget(self.guests_button)

        button_layout = QHBoxLayout()
        button_layout.addStretch(1)
        self.next_button = QPushButton("Добавить заказ")
        button_layout.addWidget(self.next_button)
        self.next_button.setFixedHeight(30)
        # if self.selected_table is None or self.selected_guests == 0:
        #     self.next_button.setEnabled(False)
        # else:
        self.next_button.clicked.connect(lambda: add_order_in_window(self, id_order=self.id_order, table_id=self.selected_table, guests=self.selected_guests))

            

        main_layout.addLayout(guest_layout)
        main_layout.setSpacing(60)
        main_layout.addLayout(table_layout)
        # main_layout.addStretch()
        main_layout.addLayout(button_layout)

        self.setLayout(main_layout)