def open_order_list_window(self):
    from view.order_list_window import OrderListWindow
    self.order_list_window = OrderListWindow()
    self.order_list_window.show()
    self.close()


def open_add_staff_window(self):
    from view.add_staff_window import AddStaffWindow
    self.add_staff_window = AddStaffWindow()
    self.add_staff_window.show()
    self.close()


def open_staff_info_window(self, staff):
    from view.staff_info_window import StaffInfoWindow
    self.staff_info_window = StaffInfoWindow(staff)
    self.staff_info_window.show()
    self.close()


def open_menu_management_window(self):
    from view.menu_management_window import MenuManagementWindow
    self.menu_window = MenuManagementWindow()
    self.menu_window.show()
    self.close()
