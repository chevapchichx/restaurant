from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel,
    QLineEdit, QComboBox, QDoubleSpinBox, QTextEdit, QMessageBox
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
from service.dish_service import DishService
from service.user_service import UserService
from view.add_dish_w_service import *


class AddDishWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.user = UserService().authorised_user
        self.dish_service = DishService()
        self.categories = self.dish_service.get_menu_categories()
        self.ui_add_dish_window()

    def ui_add_dish_window(self):
        self.setWindowTitle("Добавление блюда")
        self.setWindowIcon(QIcon("restaurant_icon.ico"))
        # self.setGeometry(500, 300, 400, 350)
        self.setFixedSize(500, 300)

        # self.setGeometry(400, 230, 500, 400)
        # self.setFixedSize(500, 400)

        main_layout = QVBoxLayout(self)

        form_layout = QVBoxLayout()

        self.name_label = QLabel("Название блюда:")
        self.name_input = QLineEdit()
        self.name_input.setFixedHeight(25)
        form_layout.addWidget(self.name_label)
        form_layout.addWidget(self.name_input)

        self.price_label = QLabel("Цена (руб.):")
        self.price_input = QLineEdit()
        self.price_input.setFixedHeight(25)
        form_layout.addWidget(self.price_label)
        form_layout.addWidget(self.price_input)

        self.weight_label = QLabel("Вес (г):")
        self.weight_input = QLineEdit()
        self.weight_input.setFixedHeight(25)
        form_layout.addWidget(self.weight_label)
        form_layout.addWidget(self.weight_input)

        self.category_label = QLabel("Категория:")
        self.category_combo = QComboBox()
        self.category_combo.setFixedHeight(25)
        if isinstance(self.categories, list):
            self.category_combo.addItems(
                [category.name for category in self.categories])
        form_layout.addWidget(self.category_label)
        form_layout.addWidget(self.category_combo)

        self.error_label = QLabel("")
        self.error_label.setStyleSheet("color: red;")
        form_layout.addWidget(self.error_label)

        form_layout.addStretch()

        main_layout.addLayout(form_layout)

        button_layout = QHBoxLayout()

        self.add_button = QPushButton("Добавить блюдо")
        self.add_button.setFixedSize(120, 25)
        self.add_button.setStyleSheet(
            "background-color: #7b99ca; font-size: 14px; color: white; border: 0; border-radius: 5px;")
        self.add_button.clicked.connect(lambda: add_dish(self))

        self.back_button = QPushButton("Назад")
        self.back_button.setFixedSize(60, 25)
        self.back_button.setStyleSheet(
            "background-color: #7b99ca; font-size: 14px; color: white; border: 0; border-radius: 5px;")
        self.back_button.clicked.connect(
            lambda: open_menu_management_window(self))

        button_layout.addWidget(self.add_button)
        button_layout.addStretch()
        button_layout.addWidget(self.back_button)

        main_layout.addLayout(button_layout)

        self.name_input.textChanged.connect(self.validate_inputs)
        self.price_input.textChanged.connect(self.validate_inputs)
        self.weight_input.textChanged.connect(self.validate_inputs)
        self.category_combo.currentIndexChanged.connect(self.validate_inputs)

    def validate_inputs(self):
        valid = True
        self.error_label.setText("")

        if not self.name_input.text().strip():
            valid = False

        try:
            price = float(self.price_input.text().strip())
            if price <= 0:
                self.error_label.setText(
                    "Цена должна быть положительным числом")
                valid = False
        except ValueError:
            if self.price_input.text().strip():
                self.error_label.setText("Цена должна быть числом")
            valid = False

        try:
            weight = float(self.weight_input.text().strip())
            if weight <= 0:
                self.error_label.setText(
                    "Вес должен быть положительным числом")
                valid = False
        except ValueError:
            if self.weight_input.text().strip():
                self.error_label.setText("Вес должен быть числом")
            valid = False

        if self.category_combo.currentIndex() < 0:
            valid = False

        self.add_button.setEnabled(valid)
