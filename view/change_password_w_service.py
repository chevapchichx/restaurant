from PyQt6.QtWidgets import QMessageBox

from service.user_service import UserService


def change_password(self):
    user_service = UserService()
    current_password = self.current_password_input.text()
    new_password = self.new_password_input.text()
    confirm_password = self.confirm_password_input.text()
    
    if not current_password or not new_password or not confirm_password:
        QMessageBox.warning(self, "Ошибка", "Пожалуйста, заполните все поля")
        return
    
    if new_password != confirm_password:
        QMessageBox.warning(self, "Ошибка", "Новый пароль и подтверждение не совпадают")
        return
    
    if not user_service.verify_password(current_password):
        QMessageBox.warning(self, "Ошибка", "Неверный текущий пароль")
        return
    
    if len(new_password) < 6:
        QMessageBox.warning(self, "Ошибка", "Пароль должен содержать минимум 6 символов")
        return
        
    result = user_service.update_password(new_password)
    
    if result:
        QMessageBox.information(self, "Успех", "Пароль успешно изменен")
        self.close()
    else:
        QMessageBox.warning(self, "Ошибка", "Не удалось изменить пароль") 