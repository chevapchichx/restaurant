def open_user_info_window(self):
    from view.user_info_window import UserInfoWindow
    self.user_info_window = UserInfoWindow()
    self.user_info_window.show()
    self.close()


def open_order_list_window(self):
    from view.order_list_window import OrderListWindow
    self.order_list_window = OrderListWindow()
    self.order_list_window.show()
    self.close()


def open_add_dish_window(self):
    from view.add_dish_window import AddDishWindow
    self.add_dish_window = AddDishWindow()
    self.add_dish_window.show()
    self.close()
