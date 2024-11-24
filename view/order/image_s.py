from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout, QMessageBox, QApplication
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt
import sys
import os

# Add project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from service.database_service import Database_Service
import io
from PIL import Image

class ImageWindow(QWidget):
    def __init__(self, dish_id):
        super().__init__()
        self.db_service = Database_Service()
        self.image_data = self.db_service.get_image_from_db(dish_id)
        if self.image_data:
            self.initUI()
        else:
            QMessageBox.warning(self, "Ошибка", "Изображение не найдено")
            self.close()

    def initUI(self):
        self.setWindowTitle('Изображение блюда')
        self.setFixedSize(400, 300)

        layout = QVBoxLayout()
        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        try:
            image = Image.open(io.BytesIO(self.image_data))
            img_byte_arr = io.BytesIO()
            image.save(img_byte_arr, format='PNG')
            pixmap = QPixmap()
            pixmap.loadFromData(img_byte_arr.getvalue())
            
            scaled_pixmap = pixmap.scaled(380, 280, 
                                        Qt.AspectRatioMode.KeepAspectRatio,
                                        Qt.TransformationMode.SmoothTransformation)
            self.image_label.setPixmap(scaled_pixmap)
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка при загрузке изображения: {str(e)}")
            
        layout.addWidget(self.image_label)
        self.setLayout(layout)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ImageWindow(1)  # Test with dish_id = 1
    window.show()
    sys.exit(app.exec())

    # def get_image_from_db(self, dish_id):
    #     try:
    #         with self.__engine.connect() as conn:
    #             query = text("SELECT photo FROM menu WHERE id_meal = :id")
    #             result = conn.execute(query, {"id": dish_id}).fetchone()
    #             return result[0] if result else None
    #     except Exception as e:
    #         print(f"Ошибка при получении изображения: {str(e)}")
    #         return None