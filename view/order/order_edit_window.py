from PyQt6.QtWidgets import QWidget, QHBoxLayout, QLabel, QPushButton, QApplication, QDialog, QVBoxLayout
from PyQt6.QtCore import Qt
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from view.order.order_edit_w_service import *
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
        top_layout.addStretch() 
        self.table_label = QLabel(f"Стол {self.order.table.id_table}, Количество гостей: {self.order.guests}")
        self.table_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        top_layout.addWidget(self.table_label)
        top_layout.addStretch() 
        main_layout.addLayout(top_layout)

        label_layout = QVBoxLayout()
        label_layout.setSpacing(2)

        for i, dish in enumerate(self.order.dishes):
            dish_label = QLabel(f"{i + 1}. {dish.dish_name}: x{dish.amount} - {dish.price} руб.")
            dish_label.setStyleSheet("margin: 0px; padding: 0px;")
            label_layout.addWidget(dish_label)

        total_sum_label = QLabel(f"Сумма: {self.order.total_sum} руб.")
        label_layout.addWidget(total_sum_label)


        # self.price_label = QLabel(f"Сумма: {self.order.price}")
        # self.status_label = QLabel(f"Статус: {self.order.status_name}")

        # label_layout.addWidget(self.price_label)
        # label_layout.addWidget(self.status_label)

        button_layout = QHBoxLayout()
        button_layout.addStretch()
        self.back_button = QPushButton("Назад")
        self.back_button.clicked.connect(self.close)
        button_layout.addWidget(self.back_button)

        main_layout.addLayout(label_layout)
        main_layout.addLayout(button_layout)
        self.setLayout(main_layout)

# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     window = Order_Edit_Window(1)  
#     window.show()
#     sys.exit(app.exec())