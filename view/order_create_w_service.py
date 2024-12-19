from PyQt6.QtWidgets import QMessageBox
from service.order_service import *
from view.order_edit_window import *
from view.order_list_window import OrderListWindow

def update_table_button(self, button):
    table_id = int(button.text())
    if OrderService().get_is_table_occupied(table_id):
        QMessageBox.critical(self, "Ошибка", f"Стол {table_id} занят")
    else:
        self.selected_table = table_id
        self.table_button.setText(f"Стол: <span style='font-size: 14px; color: #558dbb; font-weight: bold;'>{button.text()}</span>")

def update_guests_button(self, button):
    guests = int(button.text())
    self.selected_guests = guests
    self.guests_button.setText(f"Количество гостей: <span style='font-size: 14px; color: #558dbb; font-weight: bold;'>{button.text()}</span>")
    update_table_buttons(self)

def update_table_buttons(self):
    for button in self.table_number_buttons:
        table_id = int(button.text())
        table_capacity = OrderService().get_table_capacity(table_id)
        if OrderService().get_is_table_occupied(table_id) or self.selected_guests > table_capacity:
            button.setEnabled(False)
        else:
            button.setEnabled(True)

def add_order_in_window(self, id_order, table_id, guests):
    order_service = OrderService()
    order = order_service.add_order(id_order, table_id, guests)
    if order is not None:
        self.order_edit_window = OrderEditWindow(order.id_order)
        self.order_edit_window.show()
        self.close()
    else:
        QMessageBox.critical(self, "Ошибка", "Заказ не добавлен")