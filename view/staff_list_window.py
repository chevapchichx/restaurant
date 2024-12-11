from PyQt6.QtWidgets import (
    QApplication, QPushButton, QVBoxLayout, QHBoxLayout, 
    QWidget, QLabel, QTableWidget, QTableWidgetItem
)
import sys
import os
# sys.path.append((os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))  #test
from PyQt6.QtCore import Qt
from view.staff_list_w_service import *
from service.user_service import UserService
from data.user_data import UserRole, User

class StaffListWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.user = UserService().authorised_user
        # self.user = user #test
        self.ui_staffs_info_window()
    
    def ui_staffs_info_window(self):
        self.setWindowTitle("Управление персоналом")
        self.setGeometry(400, 230, 650, 450)
        self.setFixedSize(680, 450)

        main_layout = QVBoxLayout(self)

        top_layout = QHBoxLayout()

        self.add_staff_button = QPushButton("Добавить сотрудника")
        self.add_staff_button.clicked.connect(lambda: open_add_staff_window(self))
        top_layout.addWidget(self.add_staff_button)
        top_layout.addStretch()

        self.back_button = QPushButton("Назад")
        self.back_button.clicked.connect(lambda: open_order_list_window(self))

        self.staffs_table = QTableWidget()
        self.staffs_table.setColumnCount(4)
        self.staffs_table.setColumnWidth(0, 210)
        self.staffs_table.setColumnWidth(1, 130)
        self.staffs_table.setColumnWidth(2, 120)
        self.staffs_table.setColumnWidth(3, 150)
        self.staffs_table.setHorizontalHeaderLabels(["ФИО", "Должность", "Роль", "Телефон"])

        self.staffs = sorted(UserService().get_staffs_info(), key=lambda x: x.last_name)
 

        self.staffs_table.setRowCount(len(self.staffs))

        for i, staff in enumerate(self.staffs):
            item_full_name = QTableWidgetItem(f"{staff.last_name} {staff.first_name} {staff.middle_name}")
            item_full_name.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.staffs_table.setItem(i, 0, item_full_name)

            item_job = QTableWidgetItem(f"{staff.job}")
            item_job.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.staffs_table.setItem(i, 1, item_job)

            item_role = QTableWidgetItem(f"{staff.role_name}")
            item_role.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.staffs_table.setItem(i, 2, item_role)

            item_phone = QTableWidgetItem(f"{staff.phone_number}")
            item_phone.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.staffs_table.setItem(i, 3, item_phone)

        self.staffs_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.staffs_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)

        # self.staffs_table.sortItems(0, Qt.SortOrder.AscendingOrder)

        self.staffs_table.cellDoubleClicked.connect(lambda: open_staff_info_window(self, self.staffs[self.staffs_table.currentRow()]))

        exit_layout = QHBoxLayout()
        exit_layout.addStretch()
        exit_layout.addWidget(self.back_button)

        main_layout.addLayout(top_layout)
        main_layout.addWidget(self.staffs_table)
        main_layout.addLayout(exit_layout)

        self.setLayout(main_layout)

if __name__ == "__main__":
    app = QApplication([])
    # user = User(
    #     id_staff=1,
    #     role=2,
    #     job="Официант",
    #     last_name="Иванов",
    #     first_name="Иван",
    #     middle_name="Иванович",
    #     birth_date="1990-11-01",
    #     address="ул. Примерная, д. 1cnhcnccnncjcnhxdxhhxbbchbchhbc",
    #     phone_number="+7 123 456 78 90",
    #     salary="50000",
    #     login="ivanov",
    #     password=""
    # )
    window = StaffListWindow()
    window.show()
    app.exec()