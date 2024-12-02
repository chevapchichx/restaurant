from PyQt6.QtWidgets import QGridLayout, QSpinBox, QHBoxLayout, QLabel, QPushButton, QApplication, QDialog, QVBoxLayout, QMessageBox, QWidget
from PyQt6.QtCore import Qt
import sys
import os
from functools import partial
from view.order_edit_w_service import *
from service.order_service import Order_Service, Dish_Status

class Order_Edit_Window(QWidget):
    def __init__(self, id_order):
        super().__init__()
        self.order = Order_Service().get_order_for_edit(id_order)
        self.UI_Order_Edit_Window()

    def UI_Order_Edit_Window(self):
        self.setWindowTitle(f"Детали заказа {self.order.order_num}")
        self.setGeometry(400, 230, 650, 450)
        self.setFixedSize(650, 450)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(10, 20, 10, 10)

        top_layout = QVBoxLayout()
        self.table_label = QLabel(f"Стол: {self.order.table.id_table}, Количество гостей: {self.order.guests}\n\nБлюда:")
        self.table_label.setAlignment(Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignVCenter)
        top_layout.addWidget(self.table_label)
        top_layout.addStretch()
        main_layout.addLayout(top_layout)

        self.label_layout = QGridLayout()
        self.label_layout.setHorizontalSpacing(25)
        self.label_layout.setVerticalSpacing(10)
        # main_layout.addLayout(self.label_layout)

        self.total_sum_label = QLabel(f"Сумма: {self.order.total_sum} руб.")

        self.update_dishes_layout()

        button_layout = QHBoxLayout()
        button_layout.addStretch()

        button_layout.addWidget(self.total_sum_label)

        self.save_button = QPushButton("Отправить на кухню")
        self.save_button.clicked.connect(lambda: save_order(self))
        button_layout.addWidget(self.save_button)

        self.back_button = QPushButton("Заказы")
        self.back_button.clicked.connect(lambda: open_order_list_window(self))
        button_layout.addWidget(self.back_button)
        
        main_layout.addStretch(0) 
        main_layout.addLayout(self.label_layout)
        main_layout.addStretch(1)  

        main_layout.addLayout(button_layout)
        self.setLayout(main_layout)

    def update_dishes_layout(self):
        for i in reversed(range(self.label_layout.count())):
            widget = self.label_layout.itemAt(i).widget()
            if widget:
                widget.deleteLater()

        self.dish_spinboxes = [] 
        for i, dish in enumerate(self.order.dishes):
            dish_label = QLabel(f"{i + 1}. {dish.dish_name}: {dish.price}")
            dish_label.setAlignment(Qt.AlignmentFlag.AlignVCenter)

            amount_label = QLabel(f"{dish.amount}")
            status_label = QLabel(f"{dish.status_name}")

            delete_button = QPushButton("Удалить")
            delete_button.setFixedSize(65, 30)
            delete_button.clicked.connect(lambda _, d=dish: delete_dish(self, d))

            self.label_layout.addWidget(dish_label, i, 0)
            self.label_layout.addWidget(status_label, i, 2)

            if dish.status == Dish_Status.CREATED:
                spinbox = QSpinBox()
                spinbox.setValue(dish.amount)
                spinbox.setFixedSize(40, 20)
                spinbox.setMinimum(0)
                spinbox.setMaximum(10)
                spinbox.valueChanged.connect(partial(update_total_sum, self))
                self.dish_spinboxes.append(spinbox)
                self.label_layout.addWidget(spinbox, i, 1, alignment=Qt.AlignmentFlag.AlignLeft)
                self.label_layout.addWidget(delete_button, i, 3)
            else:
                self.label_layout.addWidget(amount_label, i, 1, alignment=Qt.AlignmentFlag.AlignLeft)

        update_total_sum(self) 


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Order_Edit_Window(1)  
    window.show()
    sys.exit(app.exec())