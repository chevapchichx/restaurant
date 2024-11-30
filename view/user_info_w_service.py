


def open_order_list_window(self):
    from view.order_list_window import Order_List_Window
    self.waiter_window = Order_List_Window()
    self.waiter_window.show()
    self.close()