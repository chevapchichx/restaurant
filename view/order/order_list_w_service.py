import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from service.user_service import *
from service.order_service import *

def open_auth_window(self):
    from view.user.auth_window import Auth_Window
    self.auth_window = Auth_Window()
    self.auth_window.show()
    self.close()  

def open_user_info_window(self):
    from view.user.user_info_window import User_Info_Window
    self.user_info_window = User_Info_Window()
    self.user_info_window.show()
    self.close()

def open_order_edit_window(self, id_order):
    from view.order.order_edit_window import Order_Edit_Window
    self.order_details_window = Order_Edit_Window(id_order)
    self.order_details_window.exec()


# def get_order(self):
#     order_service = Order_Service()
#     result = order_service.fill_order(self.user.login)

    # if result:

