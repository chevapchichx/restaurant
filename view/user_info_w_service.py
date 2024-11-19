import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from service.user_service import get_user_info
from data.user_data import *


def load_data(self, auth_info):
    user_info = get_user_info(auth_info[0])
    if user_info:
        user = User(user_info[0], user_info[1], user_info[2], user_info[3], user_info[4], user_info[5], user_info[6], user_info[7])
    else:
        user = None

    return user


def open_waiter_order_window(self, auth_info):
    from waiter_order_window import WaiterOrderWindow
    self.waiter_window = WaiterOrderWindow(auth_info)
    self.waiter_window.show()
    self.close()