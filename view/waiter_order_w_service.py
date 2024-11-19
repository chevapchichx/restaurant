import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from service.user_service import *


def open_auth_window(self):
    from auth_window import Auth_Window
    self.auth_window = Auth_Window()
    self.auth_window.show()
    self.close()  

def open_user_info_window(self, auth_info):
    from view.user_info_window import UserInfoWindow
    self.user_info_window = UserInfoWindow(auth_info)
    self.user_info_window.show()
    self.close()