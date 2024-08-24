import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot
import RPi.GPIO as GPIO
white_GPIO = 23
blue_GPIO = 24


class App(QWidget):
    def __init__(self):
        super().__init__()
        self.title = 'PyQt5 button'
        self.left = 100
        self.top = 100
        self.width = 320
        self.height = 200
        self.initUI()
  
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        white_button = QPushButton('White Lights')
        white_button.setStyleSheet("color:blue; background-color:red;")
        white_button.pressed.connect(self.on_white_press)
        white_button.released.connect(self.on_white_release)
        
        
        layout = QVBoxLayout()
        layout.addWidget(white_button)
        
        self.setLayout(layout)
#         blue_button = QPushButton('Blue Lights', self)
#         
#         blue_button.move(100,120)
#         blue_button.pressed.connect(self.on_blue_press)
#         blue_button.released.connect(self.on_blue_release)
        self.show()

    @pyqtSlot()
    def on_white_press(self):
        GPIO.output(white_GPIO, True)
        
    @pyqtSlot()
    def on_white_release(self):
        GPIO.output(white_GPIO, False)
        
    @pyqtSlot()
    def on_blue_press(self):
        GPIO.output(blue_GPIO, True)
        
    @pyqtSlot()
    def on_blue_release(self):
        GPIO.output(blue_GPIO, False)

if __name__ == '__main__':
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(white_GPIO, GPIO.OUT)
    GPIO.setup(blue_GPIO, GPIO.OUT)
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())