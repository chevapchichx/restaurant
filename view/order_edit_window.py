from PyQt6.QtWidgets import QGridLayout, QSpinBox, QHBoxLayout, QLabel, QPushButton, QApplication, QDialog, QVBoxLayout, QMessageBox, QWidget, QComboBox
from PyQt6.QtCore import Qt
import sys
import os
from functools import partial
sys.path.append((os.path.dirname(os.path.dirname(os.path.abspath(__file__))))) #test
from view.order_edit_w_service import *
from service.order_service import Order_Service
from service.dish_service import Dish_Service
from service.user_service import User_Service
from service.dish_service import Dish_Service

class Order_Edit_Window(QDialog):
    def __init__(self, id_order):
        super().__init__()
        self.order = Order_Service().get_order_for_edit(id_order)
        self.user = User_Service().authorised_user
        self.UI_Order_Edit_Window()

    def UI_Order_Edit_Window(self):
        self.categories = Dish_Service().get_menu_categories()

        self.setWindowTitle(f"Детали заказа {self.order.order_num}")
        self.setGeometry(470, 230, 500, 450)
        self.setFixedSize(500, 450)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(10, 20, 10, 10)

        top_layout = QVBoxLayout()
        self.table_label = QLabel(f"Стол: {self.order.table.id_table}, Количество гостей: {self.order.guests}")
        self.table_label.setAlignment(Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignTop)
        top_layout.addWidget(self.table_label)
        self.dish_label = QLabel("Блюда:")
        self.dish_label.setAlignment(Qt.AlignmentFlag.AlignTop)
        top_layout.addWidget(self.dish_label)
        # top_layout.addStretch()
        main_layout.addLayout(top_layout)


        self.dish_info_layout = QGridLayout()
        self.dish_info_layout.setHorizontalSpacing(40)
        self.dish_info_layout.setVerticalSpacing(10)
        main_layout.addLayout(self.dish_info_layout)
        
        bottom_layout = QHBoxLayout()
        self.add_dish_label = QLabel("Добавить блюдо:")
        self.add_dish_label.setAlignment(Qt.AlignmentFlag.AlignBottom)
        bottom_layout.addWidget(self.add_dish_label)
        bottom_layout.setAlignment(Qt.AlignmentFlag.AlignBottom)
        main_layout.addLayout(bottom_layout)

        self.add_dish_layout = QGridLayout()
        self.add_dish_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.choose_category_combobox = QComboBox()
        self.choose_category_combobox.setBaseSize(100, 30)
        self.choose_category_combobox.addItem("Не выбрано")
        self.choose_category_combobox.addItems([category.name for category in self.categories])
        self.choose_category_combobox.activated.connect(lambda: update_dishes_combobox(self))
        self.add_dish_layout.addWidget(self.choose_category_combobox, 0, 0)

        self.choose_dish_combobox = QComboBox()
        # self.choose_dish_combobox.addItem("Не выбрано")
        self.add_dish_layout.addWidget(self.choose_dish_combobox, 0, 1)
        self.choose_dish_combobox.activated.connect(lambda: add_dish_to_order(self))
        self.choose_dish_combobox.setDisabled(True)
   
        main_layout.addLayout(self.add_dish_layout)

        self.total_sum_label = QLabel(f"Сумма: {self.order.order_sum} руб.")

        self.ui_update_dishes_layout()

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.total_sum_label)

        self.save_button = QPushButton("Отправить на кухню")
        self.save_button.clicked.connect(lambda: update_order_item_status(self))
        button_layout.addWidget(self.save_button)

        self.back_button = QPushButton("Заказы")
        self.back_button.clicked.connect(lambda: open_order_list_window(self))
        button_layout.addWidget(self.back_button)
        main_layout.addLayout(button_layout)

        self.setLayout(main_layout)

    def ui_update_dishes_layout(self):
        for i in reversed(range(self.dish_info_layout.count())):
            widget = self.dish_info_layout.itemAt(i).widget()
            if widget:
                widget.deleteLater()

        self.dish_spinboxes = {}
        for i, order_item in enumerate(self.order.order_items):
            dish_label = QLabel(f"{i + 1}. {order_item.dish.dish_name}: {order_item.dish.price} руб.")
            dish_label.setWordWrap(True)
            dish_label.setFixedSize(195, 40)
            dish_label.setAlignment(Qt.AlignmentFlag.AlignVCenter)

            status_label = QLabel(f"{order_item.status_name}")

            self.dish_info_layout.addWidget(dish_label, i, 0)
            self.dish_info_layout.addWidget(status_label, i, 2)

            delete_button = QPushButton("Удалить")
            delete_button.setFixedSize(65, 30)
            delete_button.clicked.connect(lambda _, order_item=order_item: delete_dish(self, order_item, self.order.id_order))

            # if self.user.role == User_Role.ADMIN:
            #     self.dish_info_layout.addWidget(delete_button, i, 3)
            
            self.dish_info_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        
            amount_label = QLabel(f"{order_item.amount}")

            if order_item.status == Dish_Status.CREATED:
                spinbox = QSpinBox()
                spinbox.setRange(0, 10)
                spinbox.setValue(order_item.amount)
                spinbox.valueChanged.connect(lambda: update_order_item_amount(self))
                self.dish_info_layout.addWidget(spinbox, i, 1)
                self.dish_spinboxes.update({spinbox: order_item})
                self.dish_info_layout.addWidget(delete_button, i, 3)
            else:
                self.dish_info_layout.addWidget(amount_label, i, 1)


        update_dish_sum(self) 


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Order_Edit_Window(3)  
    window.show()
    sys.exit(app.exec())