from PyQt6.QtWidgets import (
    QApplication, QPushButton, QVBoxLayout, QHBoxLayout, 
    QWidget, QLabel, QTableWidget, QTableWidgetItem, QLineEdit, QComboBox
)
import sys
import os
sys.path.append((os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))  #test
from PyQt6.QtCore import Qt
from view.add_staff_w_service import *
from service.user_service import UserService
from data.user_data import UserRole, User

class AddStaffWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.__adding_staff_mode = True
        self.ui_add_staff_window()
    
    def ui_add_staff_window(self):
        self.__adding_staff_mode = True

        self.setWindowTitle("Добавление сотрудника")
        self.setGeometry(400, 230, 650, 450)
        self.setFixedSize(680, 450)

        main_layout = QVBoxLayout(self)

        top_layout = QHBoxLayout()

        self.add_staff_button = QPushButton("Добавить сотрудника")
        self.add_staff_button.setFixedSize(180, 25)
        self.add_staff_button.setStyleSheet("background-color: #7b99ca; font-size: 14px; color: white; border: 0; border-radius: 5px;")
        self.add_staff_button.clicked.connect(lambda: update_or_add_staff(self))
        self.add_staff_button.setEnabled(False)

        self.back_button = QPushButton("Назад")
        self.back_button.setFixedSize(60, 25)
        self.back_button.setStyleSheet("background-color: #7b99ca; font-size: 14px; color: white; border: 0; border-radius: 5px;")
        self.back_button.clicked.connect(lambda: open_staff_list_window(self))

        top_layout.addWidget(self.add_staff_button)
        top_layout.addStretch()
        top_layout.addWidget(self.back_button)

        form_layout = QVBoxLayout()

        self.login_label = QLabel("Логин")
        self.login_input = QLineEdit()
        self.login_input.setFixedHeight(25)
        self.login_input.textChanged.connect(lambda: check_login(self))

        self.password_label = QLabel("Пароль")
        self.password_input = QLineEdit()
        self.password_input.setFixedHeight(25)
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)

        self.role_label = QLabel("Роль")
        self.role_input = QComboBox()
        self.role_input.setFixedHeight(25)
        self.role_input.addItems([role.name for role in UserRole])

        self.last_name_label = QLabel("Фамилия")
        self.last_name_input = QLineEdit()
        self.last_name_input.setFixedHeight(25)

        self.first_name_label = QLabel("Имя")
        self.first_name_input = QLineEdit()
        self.first_name_input.setFixedHeight(25)

        self.middle_name_label = QLabel("Отчество")
        self.middle_name_input = QLineEdit()
        self.middle_name_input.setFixedHeight(25)

        form_layout.addWidget(self.login_label)
        form_layout.addWidget(self.login_input)
        form_layout.addWidget(self.password_label)
        form_layout.addWidget(self.password_input)
        form_layout.addWidget(self.role_label)
        form_layout.addWidget(self.role_input)
        form_layout.addWidget(self.last_name_label)
        form_layout.addWidget(self.last_name_input)
        form_layout.addWidget(self.first_name_label)
        form_layout.addWidget(self.first_name_input)
        form_layout.addWidget(self.middle_name_label)
        form_layout.addWidget(self.middle_name_input)

        form_1_layout = QVBoxLayout()

        self.job_label = QLabel("Должность")
        self.job_input = QLineEdit()
        self.job_input.setFixedHeight(25)

        self.birth_date_label = QLabel("Дата рождения")
        self.birth_date_input = QLineEdit()
        self.birth_date_input.setFixedHeight(25)

        self.address_label = QLabel("Адрес")
        self.address_input = QLineEdit()
        self.address_input.setFixedHeight(25)

        self.phone_label = QLabel("Номер телефона")
        self.phone_input = QLineEdit()
        self.phone_input.setFixedHeight(25)

        self.salary_label = QLabel("Зарплата")
        self.salary_input = QLineEdit()
        self.salary_input.setFixedHeight(25)

        self.space_label = QLabel("")
        self.space_label.setFixedHeight(22)

        self.error_label = QLabel("")
        self.error_label.setFixedHeight(22)

        form_1_layout.addWidget(self.job_label)
        form_1_layout.addWidget(self.job_input)
        form_1_layout.addWidget(self.birth_date_label)
        form_1_layout.addWidget(self.birth_date_input)
        form_1_layout.addWidget(self.address_label)
        form_1_layout.addWidget(self.address_input)
        form_1_layout.addWidget(self.phone_label)
        form_1_layout.addWidget(self.phone_input)
        form_1_layout.addWidget(self.salary_label)
        form_1_layout.addWidget(self.salary_input)
        form_1_layout.addWidget(self.space_label)
        form_1_layout.addWidget(self.error_label)

        parallel_layout = QHBoxLayout()
        parallel_layout.addLayout(form_layout)
        parallel_layout.addLayout(form_1_layout)

        exit_layout = QHBoxLayout()
        exit_layout.addStretch()
        exit_layout.addWidget(self.back_button)

        main_layout.addLayout(top_layout)
        main_layout.addLayout(parallel_layout)
        main_layout.addLayout(exit_layout)

        self.setLayout(main_layout)

        self.login_input.textChanged.connect(lambda: check_fields(self))
        self.password_input.textChanged.connect(lambda: check_fields(self))
        self.role_input.currentTextChanged.connect(lambda: check_fields(self))
        self.last_name_input.textChanged.connect(lambda: check_fields(self))
        self.first_name_input.textChanged.connect(lambda: check_fields(self))
        self.middle_name_input.textChanged.connect(lambda: check_fields(self))
        self.job_input.textChanged.connect(lambda: check_fields(self))
        self.birth_date_input.textChanged.connect(lambda: check_fields(self))
        self.address_input.textChanged.connect(lambda: check_fields(self))
        self.phone_input.textChanged.connect(lambda: check_fields(self))
        self.salary_input.textChanged.connect(lambda: check_fields(self))
