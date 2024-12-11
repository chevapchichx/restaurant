def open_order_list_window(self):
    from view.order_list_window import OrderListWindow 
    self.waiter_window = OrderListWindow()
    self.waiter_window.show()
    self.close()

def open_staff_info_window(self, staff):
    from view.staff_info_window import StaffInfoWindow
    self.staff_info_window = StaffInfoWindow(staff)
    self.staff_info_window.show()
    self.close()

def open_add_staff_window(self):
    from view.add_staff_window import AddStaffWindow
    self.add_staff_window = AddStaffWindow()
    self.add_staff_window.show()
    self.close()

