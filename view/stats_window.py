from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout,
                             QLabel, QPushButton, QTableWidget, QTableWidgetItem)
from PyQt6.QtCore import Qt
from datetime import datetime
from service.order_service import OrderService
from view.stats_w_service import *


class StatsWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.order_service = OrderService()
        self.ui_stats_window()

    def ui_stats_window(self):
        self.setWindowTitle("Статистика заказов")
        self.setGeometry(400, 230, 680, 450)
        self.setFixedSize(680, 450)

        layout = QVBoxLayout()
        self.setLayout(layout)

        header = QLabel(f"Статистика на {datetime.now().strftime('%d.%m.%Y')}")
        header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(header)

        stats = self.order_service.get_today_stats()
        if stats is None:
            stats = [0, 0, 0] 

        stats_layout = QHBoxLayout()

        orders_container = QWidget()
        orders_layout = QVBoxLayout(orders_container)
        orders_title = QLabel("Выполненных заказов")
        orders_value = QLabel(str(stats[0] or 0))  # Use 0 if None
        orders_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        orders_value.setAlignment(Qt.AlignmentFlag.AlignCenter)

        orders_layout.addWidget(orders_title)
        orders_layout.addWidget(orders_value)

        avg_container = QWidget()
        avg_layout = QVBoxLayout(avg_container)
        avg_title = QLabel("Средний чек\n(по выполненным)")
        avg_value_text = f"{stats[1]:.2f} руб." if stats[1] is not None else "0.00 руб."
        avg_value = QLabel(avg_value_text)
        avg_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        avg_value.setAlignment(Qt.AlignmentFlag.AlignCenter)

        avg_layout.addWidget(avg_title)
        avg_layout.addWidget(avg_value)

        sum_container = QWidget()
        sum_layout = QVBoxLayout(sum_container)
        revenue_title = QLabel("Выручка за день\n(по выполненным)")
        revenue_value_text = f"{stats[2]:.2f} руб." if stats[2] is not None else "0.00 руб."
        revenue_value = QLabel(revenue_value_text)
        revenue_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        revenue_value.setAlignment(Qt.AlignmentFlag.AlignCenter)

        sum_layout.addWidget(revenue_title)
        sum_layout.addWidget(revenue_value)

        stats_layout.addWidget(orders_container)
        stats_layout.addWidget(avg_container)
        stats_layout.addWidget(sum_container)

        layout.addLayout(stats_layout)

        popular_dishes_label = QLabel("Популярные блюда")
        popular_dishes_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(popular_dishes_label)
        layout.addStretch()

        popular_dishes_today = self.order_service.get_popular_dishes()
        if popular_dishes_today is None:
            popular_dishes_today = []

        popular_dishes_table = QTableWidget()
        popular_dishes_table.setColumnCount(3)
        popular_dishes_table.setRowCount(len(popular_dishes_today))
        popular_dishes_table.setFixedHeight(230)
        popular_dishes_table.setHorizontalHeaderLabels(
            ["Блюдо", "Количество", "Выручка"])
        popular_dishes_table.setColumnWidth(0, 240)
        popular_dishes_table.setColumnWidth(1, 170)
        popular_dishes_table.setColumnWidth(2, 210)
        layout.addWidget(popular_dishes_table)

        for i, order_item in enumerate(popular_dishes_today):
            dish_name = QTableWidgetItem(order_item.dish.dish_name)
            dish_name.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            popular_dishes_table.setItem(i, 0, dish_name)

            dish_count = QTableWidgetItem(str(order_item.amount))
            dish_count.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            popular_dishes_table.setItem(i, 1, dish_count)

            dish_sum = QTableWidgetItem(f"{order_item.sum:.2f} руб.")
            dish_sum.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            popular_dishes_table.setItem(i, 2, dish_sum)

        button_layout = QHBoxLayout()

        export_button = QPushButton("Экспорт в Excel")
        export_button.setFixedSize(120, 25)
        export_button.setStyleSheet(
            "background-color: #7b99ca; font-size: 14px; color: white; border: 0; border-radius: 5px;")
        export_button.clicked.connect(
            lambda: export_stats_to_excel(self, stats, popular_dishes_today))
        button_layout.addWidget(export_button)

        button_layout.addStretch()

        back_button = QPushButton("Назад")
        back_button.setFixedSize(60, 25)
        back_button.setStyleSheet(
            "background-color: #7b99ca; font-size: 14px; color: white; border: 0; border-radius: 5px;")
        back_button.clicked.connect(lambda: open_order_list_window(self))
        button_layout.addWidget(back_button)
        layout.addLayout(button_layout)
