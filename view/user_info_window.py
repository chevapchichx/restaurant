from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QVBoxLayout,
    QGridLayout, QHBoxLayout, QSpacerItem, QSizePolicy
)
from PyQt6.QtCore import Qt
from service.user_service import UserService, UserRole
from data.user_data import User
from view.user_info_w_service import *


class UserInfoWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.user = UserService().authorised_user
        self.ui_user_info_window()

    def ui_user_info_window(self):
        self.setWindowTitle("Информация о пользователе")
        self.setGeometry(400, 230, 650, 450)
        self.setFixedSize(680, 450)

        main_layout = QVBoxLayout(self)

        self.name_label = QLabel(self.user.full_name)
        self.name_label.setFixedHeight(45)
        self.name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(self.name_label)

        left_spacer = QSpacerItem(
            40, 10, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        right_spacer = QSpacerItem(
            30, 10, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        details_layout = QGridLayout()
        details_layout.setHorizontalSpacing(50)
        details_layout.setVerticalSpacing(15)
        details_layout.setColumnStretch(1, 1)
        details_layout.addItem(left_spacer, 0, 0)
        details_layout.addItem(right_spacer, 0, 5)

        style_details_labels = "font-size: 14px; color: #558dbb; font-weight: bold;"

        details_layout.addWidget(QLabel("Дата рождения:"), 0, 1)
        self.birth_date_label = QLabel(
            self.user.birth_date.strftime("%d.%m.%Y"))
        self.birth_date_label.setStyleSheet(style_details_labels)
        details_layout.addWidget(self.birth_date_label, 0, 2)

        details_layout.addWidget(QLabel("Номер телефона:"), 1, 1)
        self.phone_number_label = QLabel(self.user.phone_number)
        self.phone_number_label.setStyleSheet(style_details_labels)
        details_layout.addWidget(self.phone_number_label, 1, 2)

        details_layout.addWidget(QLabel("Должность:"), 2, 1)
        self.job_label = QLabel(self.user.job)
        self.job_label.setStyleSheet(style_details_labels)
        details_layout.addWidget(self.job_label, 2, 2)

        details_layout.addWidget(QLabel("Зарплата:"), 3, 1)
        self.salary_label = QLabel(str(self.user.salary))
        self.salary_label.setStyleSheet(style_details_labels)
        details_layout.addWidget(self.salary_label, 3, 2)

        details_layout.addWidget(QLabel("Логин:"), 0, 3)
        self.login_label = QLabel(self.user.login)
        self.login_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.login_label.setStyleSheet(style_details_labels)
        details_layout.addWidget(self.login_label, 0, 4)

        details_layout.addWidget(QLabel("Адрес:"), 1, 3)
        self.address_label = QLabel(self.user.address)
        self.address_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.address_label.setStyleSheet(style_details_labels)
        self.address_label.setWordWrap(True)
        self.address_label.setFixedSize(170, 50)
        details_layout.addWidget(self.address_label, 1, 4)

        main_layout.addLayout(details_layout)

        # Добавляем кнопку смены пароля
        change_password_layout = QHBoxLayout()
        change_password_layout.addStretch()
        self.change_password_button = QPushButton("Сменить пароль")
        self.change_password_button.setFixedSize(150, 25)
        self.change_password_button.setStyleSheet(
            "background-color: #7b99ca; font-size: 14px; color: white; border: 0; border-radius: 5px;")
        self.change_password_button.clicked.connect(
            lambda: open_change_password_window(self))
        change_password_layout.addWidget(self.change_password_button)
        change_password_layout.addStretch()
        main_layout.addLayout(change_password_layout)

        back_button_layout = QHBoxLayout()
        back_button_layout.addStretch()
        self.back_button = QPushButton("Назад")
        self.back_button.setFixedSize(60, 25)
        self.back_button.setStyleSheet(
            "background-color: #7b99ca; font-size: 14px; color: white; border: 0; border-radius: 5px;")

        back_button_layout.addWidget(self.back_button)
        main_layout.addLayout(back_button_layout)

        if self.user.role == UserRole.WAITER or self.user.role == UserRole.ADMIN:
            self.back_button.clicked.connect(
                lambda: open_order_list_window(self))
        elif self.user.role == UserRole.COOK:
            self.back_button.clicked.connect(
                lambda: open_dish_list_window(self))

        self.setLayout(main_layout)
