from PyQt6.QtWidgets import (
    QApplication, QPushButton, QVBoxLayout, QHBoxLayout, 
    QWidget, QLabel, QTableWidget, QTableWidgetItem, QSpacerItem, QSizePolicy, QGridLayout
)
from PyQt6.QtCore import Qt
from view.staff_info_w_service import *
from service.user_service import UserService
from data.user_data import UserRole, User

class StaffInfoWindow(QWidget):
    def __init__(self, staff):
        super().__init__()
        self.staff = staff
        self.ui_staff_info_window()
    
    def ui_staff_info_window(self):
        self.setWindowTitle("Информация о сотруднике")
        self.setGeometry(400, 230, 650, 450)
        self.setFixedSize(680, 450)

        main_layout = QVBoxLayout(self)

        self.name_label = QLabel(self.staff.full_name)
        self.name_label.setFixedHeight(45)
        self.name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(self.name_label)

        left_spacer = QSpacerItem(40, 10, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        right_spacer = QSpacerItem(30, 10, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        details_layout = QGridLayout()
        details_layout.setHorizontalSpacing(50)
        details_layout.setVerticalSpacing(15)
        details_layout.setColumnStretch(1, 1)
        details_layout.addItem(left_spacer, 0, 0)
        details_layout.addItem(right_spacer, 0, 5)

        style_details_labels = "font-size: 14px; color: #558dbb; font-weight: bold;"

        details_layout.addWidget(QLabel("Дата рождения:"), 0, 1)
        self.birth_date_label = QLabel(self.staff.birth_date.strftime('%d-%m-%Y'))
        self.birth_date_label.setStyleSheet(style_details_labels)
        details_layout.addWidget(self.birth_date_label, 0, 2)

        details_layout.addWidget(QLabel("Номер телефона:"), 1, 1)
        self.phone_number_label = QLabel(self.staff.phone_number)
        self.phone_number_label.setStyleSheet(style_details_labels)
        details_layout.addWidget(self.phone_number_label, 1, 2)

        details_layout.addWidget(QLabel("Должность:"), 2, 1)
        self.job_label = QLabel(self.staff.job)
        self.job_label.setStyleSheet(style_details_labels)
        details_layout.addWidget(self.job_label, 2, 2)

        details_layout.addWidget(QLabel("Зарплата:"), 3, 1)
        self.salary_label = QLabel(str(self.staff.salary))
        self.salary_label.setStyleSheet(style_details_labels)
        details_layout.addWidget(self.salary_label, 3, 2)

        details_layout.addWidget(QLabel("Логин:"), 0, 3)
        self.login_label = QLabel(self.staff.login)
        self.login_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.login_label.setStyleSheet(style_details_labels)
        details_layout.addWidget(self.login_label, 0, 4)

        details_layout.addWidget(QLabel("Адрес:"), 1, 3)
        self.address_label = QLabel(self.staff.address)
        self.address_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.address_label.setStyleSheet(style_details_labels)
        self.address_label.setWordWrap(True)
        self.address_label.setFixedSize(170, 50)
        details_layout.addWidget(self.address_label, 1, 4)

        main_layout.addLayout(details_layout)

        back_button_layout = QHBoxLayout()
        back_button_layout.addStretch()

        self.delete_staff_button = QPushButton("Скрыть сотрудника")
        self.delete_staff_button.setFixedSize(150, 25)
        self.delete_staff_button.setStyleSheet("background-color: #7b99ca; font-size: 14px; color: white; border: 0; border-radius: 5px;")
        self.delete_staff_button.clicked.connect(lambda: delete_staff(self))
        back_button_layout.addWidget(self.delete_staff_button)

        self.back_button = QPushButton("Назад")
        self.back_button.setFixedSize(60, 25)
        self.back_button.setStyleSheet("background-color: #7b99ca; font-size: 14px; color: white; border: 0; border-radius: 5px;")
        self.back_button.clicked.connect(lambda: open_staff_list_window(self))
        back_button_layout.addWidget(self.back_button)
        main_layout.addLayout(back_button_layout)     