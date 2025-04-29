def open_order_list_window(self):
    from view.order_list_window import OrderListWindow
    self.order_list = OrderListWindow()
    self.order_list.show()
    self.close()
