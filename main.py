import sys 
from PyQt6.QtWidgets import QApplication, QWidget, QLabel
from PyQt6.QtGui import QPixmap

class EmptyWindow(QWidget): 
    def __init__(self):
        """Конструктор для класса "Пустое окно"""
        super().__init__()
        self.initializeUI() 
        
    def initializeUI(self): 
        """Настройка приложения."""
        self.setGeometry(200, 100, 400, 300)
        self.setWindowTitle("Моё окно c картинкой в PyQt")
        self.setUpMainWindow()
        self.show() # Отображение окна на экране

    def setUpMainWindow(self):
        """Создайте QLabel для отображения в главном окне.""" 
        hello_label = QLabel(self) 
        hello_label.setText("Привет!")

        hello_label.move(155, 15) 
        image = "images/smile.jpg" 
        try: 
            with open(image): 
                world_label = QLabel(self) 
                pixmap = QPixmap(image) 
                pixmap = pixmap.scaled(300, 300) 
                world_label.setPixmap(pixmap) 
                world_label.move(25, 40)

        except FileNotFoundError as error: 
            print(f"Image not found.\nError: {error}")
        
# Запустить программу

if __name__ == '__main__': 
    app = QApplication(sys.argv) 
    window = EmptyWindow() 
    sys.exit(app.exec())
