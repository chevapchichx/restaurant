from PyQt6.QtWidgets import (
    QGridLayout, QSpinBox, QHBoxLayout, QLabel, QPushButton,
    QApplication, QDialog, QVBoxLayout, QMessageBox, QWidget, QComboBox, QScrollArea
)
from PyQt6.QtCore import Qt, pyqtSignal
from view.order_edit_w_service import *
from data.order_data import OrderStatus
from service.order_service import OrderService
from service.dish_service import DishService
from service.user_service import UserService
from service.dish_service import DishService

class OrderEditWindow(QWidget): 
    def __init__(self, id_order):
        super().__init__()
        self.order = OrderService().get_order_for_edit(id_order)
        self.user = UserService().authorised_user
        self.adding_dish_mode = True
        self.ui_order_edit_window()  

    def ui_order_edit_window(self): 
        if self.order.status == OrderStatus.COOKED:
            self.adding_dish_mode = False
        else:
            self.adding_dish_mode = True

        self.categories = DishService().get_menu_categories()

        self.setWindowTitle(f"Детали заказа {self.order.order_num}")
        self.setGeometry(400, 230, 680, 450)
        self.setFixedSize(680, 450)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(10, 20, 10, 10)

        top_layout = QVBoxLayout()
        self.table_label = QLabel(f"Стол: {self.order.table.id_table}, Количество гостей: {self.order.guests}")
        self.table_label.setAlignment(Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignTop)
        top_layout.addWidget(self.table_label)
        self.dish_label = QLabel("Блюда:")
        self.dish_label.setAlignment(Qt.AlignmentFlag.AlignTop)
        top_layout.addWidget(self.dish_label)
        main_layout.addLayout(top_layout)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)
        scroll_area.setWidget(scroll_content)

        self.dish_info_layout = QGridLayout()
        self.dish_info_layout.setHorizontalSpacing(40)
        self.dish_info_layout.setVerticalSpacing(10)
        scroll_layout.addLayout(self.dish_info_layout)
        main_layout.addWidget(scroll_area)
        
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
        self.add_dish_layout.addWidget(self.choose_dish_combobox, 0, 1)
        self.choose_dish_combobox.activated.connect(lambda: add_dish_to_order(self))
        self.choose_dish_combobox.setDisabled(True)
   
        main_layout.addLayout(self.add_dish_layout)

        self.total_sum_label = QLabel(f"Итого: {self.order.order_sum} руб.")

        self.ui_update_dishes_layout()

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.total_sum_label)

        self.update_or_pay_button = QPushButton("Отправить на кухню")
        self.update_or_pay_button.setFixedSize(140, 25)
        self.update_or_pay_button.setStyleSheet("background-color: #7b99ca; font-size: 14px; color: white; border: 0; border-radius: 5px;")
        self.update_or_pay_button.clicked.connect(lambda: update_or_pay_order(self))
        button_layout.addWidget(self.update_or_pay_button)

        # if self.order.status == OrderStatus.COOKED:
        #     button_layout.addWidget(self.pay_button)
        # elif self.order.status == OrderStatus.CREATED or self.order.status == OrderStatus.COOKING:
        #     button_layout.addWidget(self.save_button)

        self.back_button = QPushButton("Заказы")
        self.back_button.setFixedSize(80, 25)
        self.back_button.setStyleSheet("background-color: #7b99ca; font-size: 14px; color: white; border: 0; border-radius: 5px;")
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
            dish_label = QLabel(f"{i + 1}. {order_item.dish.dish_name}")
            dish_label.setWordWrap(True)
            dish_label.setFixedSize(200, 40)
            dish_label.setAlignment(Qt.AlignmentFlag.AlignVCenter)

            price_label = QLabel(f"{order_item.dish.price} руб.")
            price_label.setFixedSize(70, 30)
            price_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

            amount_label = QLabel(f"{order_item.amount}")
            amount_label.setFixedSize(40, 30)

            status_label = QLabel(f"{order_item.status_name}")
            status_label.setFixedSize(90, 30)
            status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

            self.dish_info_layout.addWidget(dish_label, i, 0)
            self.dish_info_layout.addWidget(price_label, i, 1)
            self.dish_info_layout.addWidget(status_label, i, 3)

            delete_button = QPushButton("Удалить")
            delete_button.setFixedSize(65, 30)
            delete_button.clicked.connect(lambda _, order_item=order_item: delete_dish(self, order_item, self.order.id_order))

            if self.user.role == UserRole.ADMIN:
                delete_button.setFixedSize(65, 30)
                self.dish_info_layout.addWidget(delete_button, i, 4)
            
            self.dish_info_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

            if order_item.status == DishStatus.CREATED:
                delete_button.setFixedSize(65, 30)
                spinbox = QSpinBox()
                spinbox.setFixedSize(40, 30)
                spinbox.setValue(order_item.amount)
                spinbox.valueChanged.connect(lambda: update_order_item_amount(self))
                self.dish_info_layout.addWidget(spinbox, i, 2)
                self.dish_spinboxes.update({spinbox: order_item})
                self.dish_info_layout.addWidget(delete_button, i, 4)
            else:
                self.dish_info_layout.addWidget(amount_label, i, 2)

        update_dish_sum(self) 