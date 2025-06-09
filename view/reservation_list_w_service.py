def open_order_list_window(self):
    from view.order_list_window import OrderListWindow
    self.order_list_window = OrderListWindow()
    self.order_list_window.show()
    self.close()


def open_add_reservation_window(self):
    from view.add_reservation_window import AddReservationWindow
    self.add_reservation_window = AddReservationWindow()
    self.add_reservation_window.show()
    self.close()
