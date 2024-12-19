from PyQt6.QtCore import QTimer
import datetime
import weakref
from service.order_service import *
from data.order_item_data import DishStatus

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

def update_item_order_status(self, order_item):
    order_service = OrderService()
    order_service.update_item_order_status(order_item, DishStatus.COOKED)
    order_service.check_or_update_order_items_status_in_order(order_item.id_order)
    self.order_items = order_service.get_order_items()
    self.ui_update_dish_list_table()

def start_timer(self, item_dish_time, added_time):
    item_dish_time_ref = weakref.ref(item_dish_time)
    timer = QTimer(self)
    timer.timeout.connect(lambda: self.update_time(item_dish_time_ref, added_time))
    timer.start(1000)

def update_time(self, item_dish_time_ref, added_time):
    item_dish_time = item_dish_time_ref()
    if item_dish_time is not None:
        elapsed_time = datetime.datetime.now() - added_time
        item_dish_time.setText(str(elapsed_time).split('.')[0])