import sys
import os
sys.path.append((os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from service.user_service import *
from service.order_service import *
from view.order_edit_window import *
from view.user_info_window import *
from auth_window import *


def open_auth_window(self):
    from auth_window import Auth_Window
    self.auth_window = Auth_Window()
    self.auth_window.show()
    self.close()  

def open_user_info_window(self):
    self.user_info_window = User_Info_Window()
    self.user_info_window.show()
    self.close()

def open_order_edit_window(self, id_order):
    self.order_details_window = Order_Edit_Window(id_order)
    self.order_details_window.exec()


# def get_order(self):
#     order_service = Order_Service()
#     result = order_service.fill_order(self.user.login)

    # if result:

