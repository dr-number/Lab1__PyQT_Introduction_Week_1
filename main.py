import sys
import os
import json
import re
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QHBoxLayout, QVBoxLayout
)
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt
from traceback import format_exc
from PyQt6.QtWidgets import QMessageBox


def natural_sort_key(text):
    def convert(text):
        return int(text) if text.isdigit() else text.lower()
    
    return [convert(c) for c in re.split('([0-9]+)', text)]

class ImageSlider(QWidget):
    __IMAGES_FOLDER = "images"
    __VALID_EXTENSIONS = ('.jpg', '.jpeg', '.png', '.gif', '.bmp')

    def __init__(self):
        '''Инициализация слайдера'''
        super().__init__()
        self.current_image_index = 0
        self.images = []
        self.title = '(название не найдено)'
        self.text_description = {}

        '''Чтение данных из файла'''
        try:
            with open('info.json', 'r', encoding='utf-8') as file:
                data = json.load(file)
                self.text_description = data.get('text_description', {})
                self.title = data.get('title', '(название не найдено)')
        except Exception as e:
            QMessageBox.critical(
                self,
                "Ошибка",
                f"Ошибка открытия файла info.json\nНажмите ОК чтобы продолжить:\n\n{e}\n{format_exc()}",
                QMessageBox.StandardButton.Ok
            )

        self.initializeUI()
        
    def initializeUI(self):
        '''Настройка графического интерфейса приложения.'''
        self.setGeometry(200, 100, 500, 400)
        self.setWindowTitle(self.title)
        self.loadImages()
        self.setUpMainWindow()
        self.show()
    
    def loadImages(self):
        '''Загрузка изображений из директории __IMAGES_FOLDER'''
        try:
            if os.path.exists(self.__IMAGES_FOLDER):
                self.images = [f for f in os.listdir(self.__IMAGES_FOLDER) if f.lower().endswith(self.__VALID_EXTENSIONS)]
                self.images.sort(key=natural_sort_key)
                
                if not self.images:
                    print(f"В папке {self.__IMAGES_FOLDER} нет изображений")
            else:
                print(f"Папка {self.__IMAGES_FOLDER} не найдена")
        except Exception as e:
            print(f"Ошибка при загрузке изображений: {e}\n{format_exc()}")
    
    def setUpMainWindow(self):
        '''Создание элементов управления в главном окне'''
        main_layout = QVBoxLayout()
        self.text_label = QLabel(self) 
        self.text_label.move(155, 15) 

        self.image_label = QLabel(self)
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image_label.setMinimumSize(1000, 600)
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
        main_layout.addWidget(self.text_label)
        main_layout.addLayout(button_layout)
        
        # Установка layout для окна
        self.setLayout(main_layout)
        self.showCurrentImage()
    
    def showCurrentImage(self):
        '''Отображение изображения'''
        if not self.images:
            self.image_label.setText("Нет изображений для отображения")
            return False
            
        try:
            key_image = self.images[self.current_image_index]
            image_path = os.path.join("images", key_image)
            pixmap = QPixmap(image_path)
            
            if not pixmap.isNull():
                scaled_pixmap = pixmap.scaled(
                    900, 600,
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation
                )
                self.image_label.setPixmap(scaled_pixmap)
                self.text_label.setText(self.text_description.get(key_image, '(описание не найдено)'))
                
                # Обновление состояния кнопок
                self.updateButtonState()
            else:
                self.image_label.setText(f"Не удалось загрузить изображение:\n{self.images[self.current_image_index]}")
                return False
                
        except Exception as e:
            print(f"Ошибка при загрузке изображения: {e}\n{format_exc()}")
            return False
        
        return True
    
    def showPreviousImage(self):
        '''Показать предыдущее изображение'''
        self.loadImages()
        if self.current_image_index > 0:
            self.current_image_index -= 1
            self.showCurrentImage()
    
    def showNextImage(self):
        '''Показать следующее изображение'''
        self.loadImages()
        if self.current_image_index < len(self.images) - 1:
            self.current_image_index += 1
            self.showCurrentImage()
    
    def updateButtonState(self):
        '''Управление доступностью кнопок'''
        self.prev_button.setEnabled(self.current_image_index > 0)
        self.next_button.setEnabled(self.current_image_index < len(self.images) - 1)

# Запуск программы
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ImageSlider()
    sys.exit(app.exec())
