from PyQt6.QtWidgets import (QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QGridLayout, QHBoxLayout)
from PyQt6.QtCore import Qt
import sys
from user_info_w_service import *


class UserInfoWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.user = User_Service().authorised_user
        self.UI_UserInfoWindow()

    def UI_UserInfoWindow(self):
        self.setWindowTitle("Информация о сотруднике")
        self.setGeometry(100, 100, 600, 450)
        self.setFixedSize(600, 450)

        main_layout = QVBoxLayout(self)

        self.name_label = QLabel(self.user.full_name)
        self.name_label.setFixedHeight(40)
        self.name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(self.name_label)

        details_layout = QGridLayout()
        details_layout.setHorizontalSpacing(20)
        details_layout.setVerticalSpacing(10)

        # label_style = """
        #     QLabel {
        #         border: 1px solid gray;
        #         border-radius: 4px;
        #         padding: 5px;
        #         min-width: 150px;
        #         min-height: 30px;
        #     }
        # """

        details_layout.addWidget(QLabel("Дата рождения:"), 0, 0)
        self.birth_date_label = QLabel(self.user.birth_date)
        # self.birth_date_label.setStyleSheet(label_style)
        details_layout.addWidget(self.birth_date_label, 0, 1)

        details_layout.addWidget(QLabel("Номер телефона:"), 1, 0)
        self.phone_number_label = QLabel(self.user.phone_number)
        # self.phone_number_label.setStyleSheet(label_style)
        details_layout.addWidget(self.phone_number_label, 1, 1)

        details_layout.addWidget(QLabel("Должность:"), 2, 0)
        self.position_label = QLabel(self.user.job)
        # self.position_label.setStyleSheet(label_style)
        details_layout.addWidget(self.position_label, 2, 1)

        details_layout.addWidget(QLabel("Зарплата:"), 3, 0)
        self.salary_label = QLabel(str(self.user.salary))
        # self.salary_label.setStyleSheet(label_style)
        details_layout.addWidget(self.salary_label, 3, 1)

        details_layout.addWidget(QLabel("Адрес:"), 0, 2)
        self.address_label = QLabel(self.user.address)
        # self.address_label.setStyleSheet(label_style)
        self.address_label.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        self.address_label.setWordWrap(True)
        self.address_label.setFixedSize(200, 80)
        details_layout.addWidget(self.address_label, 0, 3, 4, 1)

        main_layout.addLayout(details_layout)

        back_button_layout = QHBoxLayout()
        back_button_layout.addStretch()
        self.back_button = QPushButton("Назад")
        back_button_layout.addWidget(self.back_button)
        main_layout.addLayout(back_button_layout)

        self.back_button.clicked.connect(lambda: open_waiter_order_window(self))


# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     # Пример данных пользователя для тестирования
#     user = User(
#         post="Официант",
#         last_name="Иванов",
#         first_name="Иван",
#         middle_name="Иванович",
#         birth_date="01.01.1990",
#         address="ул. Примерная, д. 1",
#         phone_number="+7 123 456 78 90",
#         salary="50000",
#         login="ivanov",
#         password=""
#     )
#     window = UserInfoWindow(user)
#     window.show()
#     sys.exit(app.exec())