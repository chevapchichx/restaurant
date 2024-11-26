from PyQt6.QtWidgets import QWidget, QHBoxLayout, QLabel, QPushButton, QApplication, QDialog, QVBoxLayout
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from view.order.order_edit_w_service import *
# from service.meal_service import Meal_Service
from service.order_service import Order_Service

class Order_Edit_Window(QDialog):
    def __init__(self, id_order):
        super().__init__()
        self.order = Order_Service().get_order_for_edit(id_order)
        self.UI_Order_Edit_Window()

    def UI_Order_Edit_Window(self):
        self.setWindowTitle(f"Детали заказа {self.order.order_num}")
        self.setGeometry(100, 100, 400, 300)
        self.setFixedSize(400, 300)

        main_layout = QVBoxLayout()

        label_layout = QHBoxLayout()

        for i, dish in enumerate(self.order.dishes):
            dish_label = QLabel(f"{i + 1}. {dish.dish_name}")
            label_layout.addWidget(dish_label)

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
#     window = Order_Edit_Window(3)  
#     window.show()
#     sys.exit(app.exec())