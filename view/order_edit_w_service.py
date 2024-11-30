
def open_order_list_window(self):
    from view.order_list_window import Order_List_Window
    self.waiter_window = Order_List_Window()  
    self.close()

def update_total_sum(self):
    total_sum = 0
    for i, spinbox in enumerate(self.dish_spinboxes):
        amount = spinbox.value()
        price = self.order.dishes[i].price
        total_sum += amount * price
