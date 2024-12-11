from service.user_service import UserService
from PyQt6.QtWidgets import QMessageBox

def open_staff_list_window(self):
    from view.staff_list_window import StaffListWindow
    self.staff_list_window = StaffListWindow()
    self.staff_list_window.show()
    self.close()

def check_fields(self):
    if (self.login_input.text() and self.password_input.text() and self.role_input.currentText() and
    self.last_name_input.text() and self.first_name_input.text() and self.middle_name_input.text() and
    self.job_input.text() and self.birth_date_input.text() and self.address_input.text() and
    self.phone_input.text() and self.salary_input.text()):
        self.add_staff_button.setEnabled(True)
    else:
        self.add_staff_button.setEnabled(False)

def update_or_add_staff(self):
    if self.__adding_staff_mode == True:
        add_staff(self)
    else:
        update_staff(self)


def add_staff(self):
    login = self.login_input.text()
    password = self.password_input.text()
    role = self.role_input.currentText()
    last_name = self.last_name_input.text()
    first_name = self.first_name_input.text()
    middle_name = self.middle_name_input.text()
    job = self.job_input.text()
    birth_date = self.birth_date_input.text()
    address = self.address_input.text()
    phone_number = self.phone_input.text()
    salary = self.salary_input.text()

    if not phone_number.startswith("+7") or len(phone_number) != 16:
        self.error_label.setText("Некорректный номер телефона!")
        self.phone_input.clear()
        return
    
    if not salary.isdigit():
        self.error_label.setText("Зарплата должна быть числом!")
        self.salary_input.clear()
        return
    
    if UserService().add_staff(login, password, role, last_name, first_name, middle_name, job, birth_date, address, phone_number, salary) == "":
        open_staff_list_window(self)
        # self.close()
    else:
        self.error_label.setText("Что-то пошло не так!")

def update_staff(self):
    login = self.login_input.text()
    password = self.password_input.text()
    role = self.role_input.currentText()
    last_name = self.last_name_input.text()
    first_name = self.first_name_input.text()
    middle_name = self.middle_name_input.text()
    job = self.job_input.text()
    birth_date = self.birth_date_input.text()
    address = self.address_input.text()
    phone_number = self.phone_input.text()
    salary = self.salary_input.text()

    if not phone_number.startswith("+7") or len(phone_number) != 16:
        self.error_label.setText("Некорректный номер телефона!")
        return
    
    if not salary.isdigit():
        self.error_label.setText("Зарплата должна быть числом!")
        return
    
    if UserService().update_staff(login, password, role, last_name, first_name, middle_name, job, birth_date, address, phone_number, salary) == "":
        open_staff_list_window(self)
        # self.close()
    else:
        self.error_label.setText("Что-то пошло не так!")

def check_login(self):
    self.__adding_staff_mode = False
    login = self.login_input.text()
    staff = UserService().check_exist_login(login)
    if staff:
        if staff.role == 1:
            self.error_label.setText("Логин занят!")
        elif staff.role == 0:
            msg = QMessageBox.question(self, "Подтверждение", f"Восстановить {staff.last_name} {staff.first_name} {staff.middle_name}?", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            if msg == QMessageBox.StandardButton.Yes:
                UserService().update_deleted_status_staff(staff.id_staff)
                staff = UserService().get_staff_info_by_login(login)
                self.login_input.setText(staff.login)
                self.role_input.setCurrentText(staff.role_name)
                self.last_name_input.setText(staff.last_name)
                self.first_name_input.setText(staff.first_name)
                self.middle_name_input.setText(staff.middle_name)
                self.job_input.setText(staff.job)
                self.birth_date_input.setText(staff.birth_date.strftime("%Y-%m-%d"))
                self.address_input.setText(staff.address)
                self.phone_input.setText(staff.phone_number)
                self.salary_input.setText(str(staff.salary))
                self.add_staff_button.setEnabled(True)
                self.error_label.setText("Сотрудник восстановлен!")
                self.add_staff_button.setText("Восстановить сотрудника")
            else:
                self.error_label.setText("")
                pass
    else:
        self.error_label.setText("")
        pass
