from service.order_service import *
from service.user_service import *

def open_auth_window(self):
    from auth_window import AuthWindow
    self.auth_window = AuthWindow()
    self.auth_window.show()
    self.close()


def open_user_info_window(self):
    from view.user_info_window import UserInfoWindow
    self.user_info_window = UserInfoWindow()
    self.user_info_window.show()
    self.close()


def open_order_edit_window(self, id_order):
    from view.order_edit_window import OrderEditWindow
    self.order_details_window = OrderEditWindow(id_order)
    self.order_details_window.show()
    self.close()


def create_new_order(self, id_staff):
    """
    Создает новый заказ и открывает окно для создания заказа.

    Аргументы:
    self - ссылка на экземпляр класса, из которого вызывается функция
    id_staff - идентификатор сотрудника, создающего заказ
    """
    from view.order_create_window import OrderCreateWindow  # Импортируется окно создания заказа
    # Создается экземпляр OrderService для работы с заказами
    order_service = OrderService()
    # Вызывается метод для создания нового заказа
    new_order = order_service.create_new_order(id_staff)

    if new_order:  # Если заказ успешно создан
        # Создается и отображается окно создания заказа, передавая идентификатор и номер заказа
        self.create_order_window = OrderCreateWindow(
            new_order[0], new_order[1])
        self.create_order_window.show()
        self.close()  # Закрывается текущее окно списка заказов
    else:
        # Если заказ не удалось создать, отображается сообщение об ошибке
        QMessageBox.critical(self, "Ошибка", "Не удалось создать новый заказ")


def open_staff_list_window(self):
    from view.staff_list_window import StaffListWindow
    self.staff_list_window = StaffListWindow()
    self.staff_list_window.show()
    self.close()


def open_stats_window(self):
    from view.stats_window import StatsWindow
    self.stats_window = StatsWindow()
    self.stats_window.show()
    self.close()


def open_menu_management_window(self):
    from view.menu_management_window import MenuManagementWindow
    self.menu_window = MenuManagementWindow()
    self.menu_window.show()
    self.close()


def open_reservation_list_window(self):
    from view.reservation_list_window import ReservationListWindow
    self.reservation_list_window = ReservationListWindow()
    self.reservation_list_window.show()
    self.close()
