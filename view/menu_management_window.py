from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel,
    QTableWidget, QTableWidgetItem, QComboBox
)
from PyQt6.QtCore import Qt
from service.dish_service import DishService
from service.user_service import UserService
from view.menu_management_w_service import *


class MenuManagementWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.user = UserService().authorised_user
        self.dish_service = DishService()
        self.categories = self.dish_service.get_menu_categories()
        self.ui_menu_management_window()

    def ui_menu_management_window(self):
        self.setWindowTitle("Управление меню")
        self.setGeometry(400, 230, 680, 450)
        self.setFixedSize(680, 450)

        main_layout = QVBoxLayout(self)

        top_layout = QHBoxLayout()

        self.add_dish_button = QPushButton("Добавить блюдо")
        self.add_dish_button.setFixedSize(150, 25)
        self.add_dish_button.setStyleSheet(
            "background-color: #7b99ca; font-size: 14px; color: white; border: 0; border-radius: 5px;")
        self.add_dish_button.clicked.connect(
            lambda: open_add_dish_window(self))

        self.back_button = QPushButton("Назад")
        self.back_button.setFixedSize(60, 25)
        self.back_button.setStyleSheet(
            "background-color: #7b99ca; font-size: 14px; color: white; border: 0; border-radius: 5px;")
        self.back_button.clicked.connect(lambda: open_order_list_window(self))

        top_layout.addWidget(self.add_dish_button)
        top_layout.addStretch()

        category_filter_layout = QHBoxLayout()
        category_label = QLabel("Категория:")
        self.category_combo = QComboBox()
        self.category_combo.addItem("Все категории")
        if isinstance(self.categories, list):
            self.category_combo.addItems(
                [category.name for category in self.categories])
        self.category_combo.currentIndexChanged.connect(self.filter_dishes)

        category_filter_layout.addWidget(category_label)
        category_filter_layout.addWidget(self.category_combo)

        top_layout.addLayout(category_filter_layout)
        top_layout.addWidget(self.back_button)

        main_layout.addLayout(top_layout)

        self.dish_table = QTableWidget()
        self.dish_table.setColumnCount(4)
        self.dish_table.setHorizontalHeaderLabels(
            ["Название", "Цена (руб.)", "Вес (г)", "Категория"])
        self.dish_table.setColumnWidth(0, 240)
        self.dish_table.setColumnWidth(1, 100)
        self.dish_table.setColumnWidth(2, 100)
        self.dish_table.setColumnWidth(3, 170)
        self.dish_table.setEditTriggers(
            QTableWidget.EditTrigger.NoEditTriggers)
        self.dish_table.setSelectionBehavior(
            QTableWidget.SelectionBehavior.SelectRows)

        main_layout.addWidget(self.dish_table)

        self.load_dishes()

    def load_dishes(self, category_id=None):
        dishes = self.dish_service.get_all_dishes(
        ) if category_id is None else self.dish_service.get_dishes_by_category(category_id)

        if isinstance(dishes, list):
            self.dish_table.setRowCount(len(dishes))

            for i, dish in enumerate(dishes):
                name_item = QTableWidgetItem(dish.dish_name)
                price_item = QTableWidgetItem(f"{dish.price:.2f}")
                weight_item = QTableWidgetItem(f"{dish.weight:.2f}")

                category_name = ""
                if dish.menu_category:
                    if isinstance(dish.menu_category, list):
                        if dish.menu_category:
                            category_name = dish.menu_category[0].name
                    else:
                        for cat in self.categories:
                            if cat.id_menu_category == dish.menu_category:
                                category_name = cat.name
                                break

                category_item = QTableWidgetItem(category_name)

                self.dish_table.setItem(i, 0, name_item)
                self.dish_table.setItem(i, 1, price_item)
                self.dish_table.setItem(i, 2, weight_item)
                self.dish_table.setItem(i, 3, category_item)
        else:
            self.dish_table.setRowCount(0)

    def filter_dishes(self):
        index = self.category_combo.currentIndex()
        if index == 0: 
            self.load_dishes()
        else:
            category_id = self.categories[index - 1].id_menu_category
            self.load_dishes(category_id)