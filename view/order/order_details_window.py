from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QApplication, QDialog
import sys
from view.order.order_details_w_service import *
from service.user_service import User_Service
from service.order_service import Order_Service

class Order_Details_Window(QDialog):
    def __init__(self, id_order):
        super().__init__()
        self.order = Order_Service().fill_order_by_id(id_order)
        self.UI_Order_Details_Window()

    def UI_Order_Details_Window(self):
        self.setWindowTitle(f"Детали заказа {self.order.order_num}")
        self.setGeometry(100, 100, 400, 300)
        self.setFixedSize(400, 300)

        layout = QVBoxLayout()

        self.order_id_label = QLabel(f"ID заказа: {self.order.id_order}")
        self.order_num_label = QLabel(f"Номер заказа: {self.order.order_num}")
        self.worker_label = QLabel(f"Официант: {self.order.worker.first_name} {self.order.worker.last_name}")
        self.meal_label = QLabel(f"Блюдо: {self.order.meal}")
        self.table_label = QLabel(f"Стол: {self.order.table}")
        self.date_label = QLabel(f"Дата: {self.order.date}")
        self.time_label = QLabel(f"Время: {self.order.time}")
        self.price_label = QLabel(f"Сумма: {self.order.price}")
        self.status_label = QLabel(f"Статус: {self.order.status_name}")

        layout.addWidget(self.order_id_label)
        layout.addWidget(self.order_num_label)
        layout.addWidget(self.worker_label)
        layout.addWidget(self.meal_label)
        layout.addWidget(self.table_label)
        layout.addWidget(self.date_label)
        layout.addWidget(self.time_label)
        layout.addWidget(self.price_label)
        layout.addWidget(self.status_label)

        self.back_button = QPushButton("Назад")
        self.back_button.clicked.connect(lambda: open_order_list_window(self))
        layout.addWidget(self.back_button)

        self.setLayout(layout)

# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     window = Order_Details_Window(order=None)  # Пример, передайте реальный заказ при использовании
#     window.show()
#     sys.exit(app.exec())