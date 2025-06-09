def open_reservation_list_window(self):
    from view.reservation_list_window import ReservationListWindow
    self.reservation_list_window = ReservationListWindow()
    self.reservation_list_window.show()
    self.close()
