import sys
import os
sys.path.append((os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from service.user_service import *


def open_order_list_window(self):
    from order_list_window import Order_List_Window
    self.waiter_window = Order_List_Window()
    self.waiter_window.show()
    self.close()