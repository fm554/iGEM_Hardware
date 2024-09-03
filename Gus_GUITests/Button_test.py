import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QLabel
from PyQt5.QtGui import QIcon
from PyQt5 import QtCore
from PyQt5.QtCore import pyqtSlot
from qtwidgets import Toggle
RPi = False
# import RPi.GPIO as GPIO
# white_GPIO = 23
# blue_GPIO = 24

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
        white_button.pressed.connect(self.on_white_press)
        white_button.released.connect(self.on_white_release)

        blue_button = QPushButton('Blue Lights', self)
        blue_button.pressed.connect(self.on_blue_press)
        blue_button.released.connect(self.on_blue_release)
        
        #imaging mode layout
        imaging_mode_layout = QHBoxLayout()
        std_img_mode_label = QLabel("Standard\nImaging")
        std_img_mode_label.setAlignment(QtCore.Qt.AlignCenter)
        fluoro_img_mode_label = QLabel("Fluorescent\nImaging")
        fluoro_img_mode_label.setAlignment(QtCore.Qt.AlignCenter)
        imaging_mode_toggle = Toggle()
        imaging_mode_toggle.stateChanged.connect(lambda:self.on_image_mode_change(imaging_mode_toggle))

        imaging_mode_layout.addWidget(std_img_mode_label)
        imaging_mode_layout.addWidget(imaging_mode_toggle)
        imaging_mode_layout.addWidget(fluoro_img_mode_label)

        layout = QVBoxLayout()
        layout.addWidget(white_button)
        layout.addWidget(blue_button)
        layout.addLayout(imaging_mode_layout)
        self.setLayout(layout)
#      
            self.show()

    @pyqtSlot()
    def on_white_press(self):
        if RPi:
            GPIO.output(white_GPIO, True)
        
    @pyqtSlot()
    def on_white_release(self):
        if RPi:
            GPIO.output(white_GPIO, False)
        
    @pyqtSlot()
    def on_blue_press(self):
        if RPi:
            GPIO.output(blue_GPIO, True)
        
    @pyqtSlot()
    def on_blue_release(self):
        if RPi:
            GPIO.output(blue_GPIO, False)

    @pyqtSlot()
    def on_image_mode_change(self, btn):
        if btn.isChecked():
            print("Checked")
            # turn on blue light
            # change servo angle
        else:
            print("Unchecked")

if __name__ == '__main__':
    # GPIO.setwarnings(False)
    # GPIO.setmode(GPIO.BCM)
    # GPIO.setup(white_GPIO, GPIO.OUT)
    # GPIO.setup(blue_GPIO, GPIO.OUT)
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())