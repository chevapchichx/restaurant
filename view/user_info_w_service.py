from view.order_list_window import OrderListWindow
from view.dish_list_window import DishListWindow
from view.change_password_window import ChangePasswordWindow
from view.menu_management_window import MenuManagementWindow
from PyQt6.QtCore import Qt


def open_order_list_window(self):
    self.close()
    self.w = OrderListWindow()
    self.w.show()


def open_dish_list_window(self):
    self.close()
    self.w = DishListWindow()
    self.w.show()


def open_menu_management_window(self):
    self.close()
    self.w = MenuManagementWindow()
    self.w.show()


def open_change_password_window(self):

    self.change_password_window = ChangePasswordWindow()
    self.change_password_window.setWindowModality(
        Qt.WindowModality.WindowModal) 
    self.change_password_window.move(
        self.x() + (self.width() - self.change_password_window.width()) // 2,
        self.y() + (self.height() - self.change_password_window.height()) // 2
    )
    self.change_password_window.show()
