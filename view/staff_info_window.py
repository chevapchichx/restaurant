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

        details_layout.addWidget(QLabel("Дата рождения:"), 0, 1)
        self.birth_date_label = QLabel(self.staff.birth_date.strftime('%d-%m-%Y'))
        details_layout.addWidget(self.birth_date_label, 0, 2)

        details_layout.addWidget(QLabel("Номер телефона:"), 1, 1)
        self.phone_number_label = QLabel(self.staff.phone_number)
        details_layout.addWidget(self.phone_number_label, 1, 2)

        details_layout.addWidget(QLabel("Должность:"), 2, 1)
        self.job_label = QLabel(self.staff.job)
        details_layout.addWidget(self.job_label, 2, 2)

        details_layout.addWidget(QLabel("Зарплата:"), 3, 1)
        self.salary_label = QLabel(str(self.staff.salary))
        details_layout.addWidget(self.salary_label, 3, 2)

        details_layout.addWidget(QLabel("Адрес:"), 0, 3)
        self.address_label = QLabel(self.staff.address)
        self.address_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.address_label.setWordWrap(True)
        self.address_label.setFixedSize(170, 50)
        details_layout.addWidget(self.address_label, 0, 4)

        main_layout.addLayout(details_layout)

        back_button_layout = QHBoxLayout()
        back_button_layout.addStretch()

        self.delete_staff_button = QPushButton("Удалить сотрудника")
        self.delete_staff_button.clicked.connect(lambda: delete_staff(self))
        back_button_layout.addWidget(self.delete_staff_button)

        self.back_button = QPushButton("Назад")
        self.back_button.clicked.connect(lambda: open_staff_list_window(self))
        back_button_layout.addWidget(self.back_button)
        main_layout.addLayout(back_button_layout)


        