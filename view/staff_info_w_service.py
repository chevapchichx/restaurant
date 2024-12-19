from service.user_service import UserService
from PyQt6.QtWidgets import QMessageBox

def open_staff_list_window(self):
    from view.staff_list_window import StaffListWindow
    self.staff_list_window = StaffListWindow()
    self.staff_list_window.show()
    self.close()

def delete_staff(self):
    from view.staff_list_window import StaffListWindow
    msg = QMessageBox(self)
    msg.setWindowTitle("Подтверждение")
    msg.setText(f"Скрыть сотрудника {self.staff.full_name}?")
    msg.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
    yes_button = msg.button(QMessageBox.StandardButton.Yes)
    no_button = msg.button(QMessageBox.StandardButton.No)
    yes_button.setText("Да")
    no_button.setText("Нет")
    result = msg.exec()

    if result == QMessageBox.StandardButton.Yes:
        user_service = UserService()
        result = user_service.update_deleted_status_staff(self.staff.id_staff)
        if result == "":
            self.staff_list_window = StaffListWindow()
            self.staff_list_window.show()
            self.close()
        else:
            QMessageBox.critical(self, "Ошибка", result)
    else:
        pass