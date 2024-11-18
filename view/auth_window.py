import sys
import os
from auth_service import *
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout


class Auth_Window(QWidget):
    def __init__(self):
        super().__init__()
        # self.waiter_window = None 
        self.UI_Auth_Window()

    def UI_Auth_Window(self):      
        self.setWindowTitle("Login")
        self.setGeometry(100, 100, 400, 200)

        self.login_label = QLabel("Логин")
        self.login_input = QLineEdit()
        self.login_input.setFixedHeight(30)

        self.password_label = QLabel("Пароль")
        self.password_input = QLineEdit()
        self.password_input.setFixedHeight(30)
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)

        self.entry_button = QPushButton("Войти")
        self.entry_button.setFixedHeight(30)
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

        main_layout = QVBoxLayout()
        main_layout.addLayout(form_layout)
        main_layout.addLayout(button_layout)
        
        self.setLayout(main_layout)

        self.setFixedSize(400, 200)



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Auth_Window()
    window.show()
    sys.exit(app.exec())


# password = b'456'
 
# salt = bcrypt.gensalt()
# hashed = bcrypt.hashpw(password, salt)

# print(hashed)