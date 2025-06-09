from PyQt6.QtWidgets import (QApplication, QHBoxLayout, QLabel, QLineEdit,
                            QPushButton, QVBoxLayout, QWidget, QMessageBox)
from PyQt6.QtCore import Qt

from view.change_password_w_service import *


class ChangePasswordWindow(QWidget):    
    def __init__(self):
        super().__init__()
        self.ui_change_password_window()

    def ui_change_password_window(self):      
        self.setWindowTitle("Смена пароля")
        self.setGeometry(500, 300, 400, 250)
        self.setFixedSize(400, 300)

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 20)

        self.current_password_label = QLabel("Текущий пароль")
        self.current_password_input = QLineEdit()
        self.current_password_input.setFixedHeight(30)
        self.current_password_input.setEchoMode(QLineEdit.EchoMode.Password)

        self.new_password_label = QLabel("Новый пароль")
        self.new_password_input = QLineEdit()
        self.new_password_input.setFixedHeight(30)
        self.new_password_input.setEchoMode(QLineEdit.EchoMode.Password)

        self.confirm_password_label = QLabel("Подтвердите новый пароль")
        self.confirm_password_input = QLineEdit()
        self.confirm_password_input.setFixedHeight(30)
        self.confirm_password_input.setEchoMode(QLineEdit.EchoMode.Password)

        self.change_button = QPushButton("Сменить пароль")
        self.change_button.setFixedHeight(25)
        self.change_button.setFixedWidth(150)
        self.change_button.setStyleSheet(
            "background-color: #7b99ca; font-size: 14px; color: white; border: 0; border-radius: 5px;")
        self.change_button.clicked.connect(lambda: change_password(self))
        
        self.cancel_button = QPushButton("Отмена")
        self.cancel_button.setFixedHeight(25)
        self.cancel_button.setFixedWidth(100)
        self.cancel_button.setStyleSheet(
            "background-color: #7b99ca; font-size: 14px; color: white; border: 0; border-radius: 5px;")
        self.cancel_button.clicked.connect(self.close)
  
        form_layout = QVBoxLayout()
        form_layout.setSpacing(10)
        form_layout.addWidget(self.current_password_label)
        form_layout.addWidget(self.current_password_input)
        form_layout.addWidget(self.new_password_label)
        form_layout.addWidget(self.new_password_input)
        form_layout.addWidget(self.confirm_password_label)
        form_layout.addWidget(self.confirm_password_input)

        button_layout = QHBoxLayout()
        button_layout.setSpacing(15)
        button_layout.addStretch(1)                                                                                    
        button_layout.addWidget(self.change_button)
        button_layout.addWidget(self.cancel_button)
        button_layout.addStretch(1)

        main_layout.addLayout(form_layout)
        main_layout.addSpacing(15)
        main_layout.addLayout(button_layout)
        
        self.setLayout(main_layout) 