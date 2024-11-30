from PyQt6.QtWidgets import QSpinBox, QHBoxLayout, QLabel, QPushButton, QApplication, QDialog, QVBoxLayout
from PyQt6.QtCore import Qt
import sys
import os
from view.order_edit_w_service import *
from service.order_service import Order_Service

class Order_Edit_Window(QDialog):
    def __init__(self, id_order):
        super().__init__()
        self.order = Order_Service().get_order_for_edit(id_order)
        self.UI_Order_Edit_Window()

    def UI_Order_Edit_Window(self):
        self.setWindowTitle(f"Детали заказа {self.order.order_num}")
        self.setGeometry(520, 300, 400, 300)
        self.setFixedSize(400, 300)

        main_layout = QVBoxLayout(self)

        top_layout = QHBoxLayout()
        self.table_label = QLabel(f"Стол {self.order.table.id_table}, Количество гостей: {self.order.guests}")
        self.table_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        top_layout.addWidget(self.table_label)
        top_layout.addStretch()  
        main_layout.addLayout(top_layout)

        label_layout = QVBoxLayout()
        label_layout.setSpacing(2)

        self.dish_spinboxes = []

        for i, dish in enumerate(self.order.dishes):
            dish_layout = QHBoxLayout()
            dish_label = QLabel(f"{i + 1}. {dish.dish_name}: {dish.price}")
            dish_label.setStyleSheet("margin: 0px; padding: 0px;")
            dish_layout.addWidget(dish_label)

            spinbox = QSpinBox()
            spinbox.setValue(int(dish.amount))
            spinbox.setFixedSize(40, 20)
            spinbox.setMinimum(0)
            spinbox.setMaximum(10)
            spinbox.valueChanged.connect(lambda: update_total_sum(self))
            self.dish_spinboxes.append(spinbox)
            dish_layout.addWidget(spinbox)

            label_layout.addLayout(dish_layout)

        self.total_sum_label = QLabel(f"Сумма: {self.order.total_sum} руб.")
        label_layout.addWidget(self.total_sum_label)

        button_layout = QHBoxLayout()
        button_layout.addStretch()
        self.back_button = QPushButton("Назад")
        self.back_button.clicked.connect(self.close)
        button_layout.addWidget(self.back_button)

        main_layout.addLayout(label_layout)
        main_layout.addLayout(button_layout)
        self.setLayout(main_layout)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Order_Edit_Window(1)  
    window.show()
    sys.exit(app.exec())