def open_order_list_window(self):
    from view.order_list_window import OrderListWindow 
    self.waiter_window = OrderListWindow()
    self.waiter_window.show()
    self.close()

def open_dish_list_window(self):
    from view.dish_list_window import DishListWindow 
    self.dish_list_window = DishListWindow()
    self.dish_list_window.show()
    self.close()