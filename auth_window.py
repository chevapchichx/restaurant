import sys
from PyQt6.QtWidgets import (QApplication, QHBoxLayout, QLabel, QLineEdit,
                            QPushButton, QVBoxLayout, QWidget)

from service.user_service import UserService
from view.auth_w_service import *


class AuthWindow(QWidget):    
    def __init__(self):
        super().__init__()
        self.user = UserService().authorised_user
        self.ui_auth_window()

    def ui_auth_window(self):      
        self.setWindowTitle("Авторизация")
        self.setGeometry(500, 300, 400, 200)
        self.setFixedSize(400, 200)

        main_layout = QVBoxLayout()

        self.login_label = QLabel("Логин")
        self.login_input = QLineEdit()
        self.login_input.setFixedHeight(30)

        self.password_label = QLabel("Пароль")
        self.password_input = QLineEdit()
        self.password_input.setFixedHeight(30)
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)

        self.entry_button = QPushButton("Войти")
        self.entry_button.setFixedHeight(25)
        self.entry_button.setFixedWidth(70)
        self.entry_button.setStyleSheet("background-color: #7b99ca; font-size: 14px; color: white; border: 0; border-radius: 5px;")
        self.entry_button.clicked.connect(lambda: get_auth(self))
  
        form_layout = QVBoxLayout()
        form_layout.addWidget(self.login_label)
        form_layout.addWidget(self.login_input)
        form_layout.addWidget(self.password_label)
        form_layout.addWidget(self.password_input)

        button_layout = QHBoxLayout()
        button_layout.addStretch(1)                                                                                    
        button_layout.addWidget(self.entry_button)
        button_layout.addStretch(1)

        main_layout.addLayout(form_layout)
        main_layout.addLayout(button_layout)
        
        self.setLayout(main_layout)

        self.setFixedSize(400, 200)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AuthWindow()
    window.show()
    sys.exit(app.exec())


# password = b'1672'
# salt = bcrypt.gensalt()
# hashed = bcrypt.hashpw(password, salt)
# print(hashed)