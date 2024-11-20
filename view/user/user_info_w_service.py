import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from service.user_service import *
from data.user_data import *


# def get_user(self, user):
#     user = User_Service.get_user_db(user[0])
#     return user


def open_order_list_window(self):
    from view.user.order_list_window import Order_List_Window
    self.waiter_window = Order_List_Window()
    self.waiter_window.show()
    self.close()