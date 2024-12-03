from PyQt6.QtWidgets import QMessageBox
from service.order_service import *
from view.order_edit_window import *
from view.order_list_window import Order_List_Window

def update_table_button(self, button):
    table_id = int(button.text())
    if Order_Service().get_is_table_occupied(table_id):
        QMessageBox.critical(self, "Ошибка", f"Стол {table_id} занят")
    else:
        self.selected_table = table_id
        self.table_button.setText(f"Стол: {button.text()}")

def update_guests_button(self, button):
    guests = int(button.text())
    self.selected_guests = guests
    self.guests_button.setText(f"Количество гостей: {button.text()}")
    update_table_buttons(self)

def update_table_buttons(self):
    for button in self.table_number_buttons:
        table_id = int(button.text())
        table_capacity = Order_Service().get_table_capacity(table_id)
        if Order_Service().get_is_table_occupied(table_id) or self.selected_guests > table_capacity:
            button.setEnabled(False)
        else:
            button.setEnabled(True)

def add_order_in_window(self, id_order, table_id, guests):
    order_service = Order_Service()
    order = order_service.add_order(id_order, table_id, guests)
    if order is not None:
        self.order_edit_window = Order_Edit_Window(order.id_order)
        self.order_list_window = Order_List_Window()
        self.order_list_window.show()
        self.order_edit_window.show()
        self.close()
    else:
        QMessageBox.critical(self, "Ошибка", "Заказ не добавлен")