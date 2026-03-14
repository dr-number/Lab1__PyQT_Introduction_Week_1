import sys
import os
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QHBoxLayout, QVBoxLayout
)
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt
from traceback import format_exc

class ImageSlider(QWidget):
    __IMAGES_FOLDER = "images"
    __VALID_EXTENSIONS = ('.jpg', '.jpeg', '.png', '.gif', '.bmp')

    def __init__(self):
        super().__init__()
        self.current_image_index = 0
        self.images = []
        self.initializeUI()
        
    def initializeUI(self):
        self.setGeometry(200, 100, 500, 400)
        self.setWindowTitle("Слайдер изображений")
        self.loadImages()
        self.setUpMainWindow()
        self.show()
    
    def loadImages(self):
        try:
            if os.path.exists(self.__IMAGES_FOLDER):
                self.images = [f for f in os.listdir(self.__IMAGES_FOLDER) if f.lower().endswith(self.__VALID_EXTENSIONS)]
                self.images.sort()
                
                if not self.images:
                    print(f"В папке {self.__IMAGES_FOLDER} нет изображений")
            else:
                print(f"Папка {self.__IMAGES_FOLDER} не найдена")
        except Exception as e:
            print(f"Ошибка при загрузке изображений: {e}\n{format_exc()}")
    
    def setUpMainWindow(self):
        main_layout = QVBoxLayout()
        self.image_label = QLabel(self)
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image_label.setMinimumSize(400, 300)
        self.image_label.setStyleSheet("border: 1px solid gray;")
        
        self.prev_button = QPushButton("← Назад", self)
        self.next_button = QPushButton("Вперед →", self)
        
        self.prev_button.setFixedSize(100, 30)
        self.next_button.setFixedSize(100, 30)
        
        self.prev_button.clicked.connect(self.showPreviousImage)
        self.next_button.clicked.connect(self.showNextImage)
        
        # Горизонтальный layout для кнопок
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.prev_button)
        button_layout.addWidget(self.next_button)
        button_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Добавление виджетов в основной layout
        main_layout.addWidget(self.image_label)
        main_layout.addLayout(button_layout)
        
        # Установка layout для окна
        self.setLayout(main_layout)
        
        self.showCurrentImage()
    
    def showCurrentImage(self):
        if not self.images:
            self.image_label.setText("Нет изображений для отображения")
            return
            
        try:
            image_path = os.path.join("images", self.images[self.current_image_index])
            pixmap = QPixmap(image_path)
            
            if not pixmap.isNull():
                scaled_pixmap = pixmap.scaled(
                    450, 300,
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation
                )
                self.image_label.setPixmap(scaled_pixmap)
                
                # Обновление состояния кнопок
                self.updateButtonState()
            else:
                self.image_label.setText(f"Не удалось загрузить изображение:\n{self.images[self.current_image_index]}")
                
        except Exception as e:
            print(f"Ошибка при загрузке изображения: {e}\n{format_exc()}")
    
    def showPreviousImage(self):
        self.loadImages()
        if self.current_image_index > 0:
            self.current_image_index -= 1
            self.showCurrentImage()
    
    def showNextImage(self):
        self.loadImages()
        if self.current_image_index < len(self.images) - 1:
            self.current_image_index += 1
            self.showCurrentImage()
    
    def updateButtonState(self):
        self.prev_button.setEnabled(self.current_image_index > 0)
        self.next_button.setEnabled(self.current_image_index < len(self.images) - 1)
    
    def keyPressEvent(self, event):
        """Обработка нажатий клавиш клавиатуры"""
        if event.key() == Qt.Key.Key_Left:
            self.showPreviousImage()
        elif event.key() == Qt.Key.Key_Right:
            self.showNextImage()

# Запуск программы
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ImageSlider()
    sys.exit(app.exec())
