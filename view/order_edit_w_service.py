import sys
import os
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))   #test
from service.order_service import *

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
    self.total_sum_label.setText(f"Сумма: {total_sum} руб.")

def save_order(self):
    for i, spinbox in enumerate(self.dish_spinboxes):
        self.order.dishes[i].amount = spinbox.value()
    Order_Service().save_order_1(self.order)
    open_order_list_window(self)
