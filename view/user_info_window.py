from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, 
    QGridLayout, QHBoxLayout, QSpacerItem, QSizePolicy
)
from PyQt6.QtCore import Qt
import sys
import os
# sys.path.append((os.path.dirname(os.path.dirname(os.path.abspath(__file__))))) #test
from service.user_service import UserService, UserRole
from view.user_info_w_service import *

class UserInfoWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.user = UserService().authorised_user
        self.ui_user_info_window()

    def ui_user_info_window(self):
        self.setWindowTitle("Информация о сотруднике")
        self.setGeometry(400, 230, 650, 450)
        self.setFixedSize(680, 450)

        main_layout = QVBoxLayout(self)

        self.name_label = QLabel(self.user.full_name)
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
        self.birth_date_label = QLabel(self.user.birth_date.strftime('%d-%m-%Y'))
        details_layout.addWidget(self.birth_date_label, 0, 2)

        details_layout.addWidget(QLabel("Номер телефона:"), 1, 1)
        self.phone_number_label = QLabel(self.user.phone_number)
        details_layout.addWidget(self.phone_number_label, 1, 2)

        details_layout.addWidget(QLabel("Должность:"), 2, 1)
        self.job_label = QLabel(self.user.job)
        details_layout.addWidget(self.job_label, 2, 2)

        details_layout.addWidget(QLabel("Зарплата:"), 3, 1)
        self.salary_label = QLabel(str(self.user.salary))
        details_layout.addWidget(self.salary_label, 3, 2)

        details_layout.addWidget(QLabel("Адрес:"), 0, 3)
        self.address_label = QLabel(self.user.address)
        self.address_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.address_label.setWordWrap(True)
        self.address_label.setFixedSize(170, 50)
        details_layout.addWidget(self.address_label, 0, 4)

        main_layout.addLayout(details_layout)

        back_button_layout = QHBoxLayout()
        back_button_layout.addStretch()
        self.back_button = QPushButton("Назад")
        back_button_layout.addWidget(self.back_button)
        main_layout.addLayout(back_button_layout)

        if self.user.role == UserRole.WAITER or self.user.role == UserRole.ADMIN:
            self.back_button.clicked.connect(lambda: open_order_list_window(self))
        elif self.user.role == UserRole.COOK:
            self.back_button.clicked.connect(lambda: open_dish_list_window(self))


# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     user = User(
#         id_worker=1,
#         role=1,
#         job="Официант",
#         last_name="Иванов",
#         first_name="Иван",
#         middle_name="Иванович",
#         birth_date="1990-11-01",
#         address="ул. Примерная, д. 1cnhcnccnncjcnhxdxhhxbbchbchhbc",
#         phone_number="+7 123 456 78 90",
#         salary="50000",
#         login="ivanov",
#         password=""
#     )
#     window = User_Info_Window()
#     window.show()
#     sys.exit(app.exec())