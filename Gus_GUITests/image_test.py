# importing the required libraries

from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt, QEvent
import sys
from PIL import Image, ImageQt


class Window(QMainWindow):
	def __init__(self):
		super().__init__()
		self.windowWidth = 400
		self.windowHeight = 300
		self.acceptDrops()
		# set the title
		self.setWindowTitle("Image")

		# setting the geometry of window
		self.setGeometry(0, 0, 400, 300)

		# creating label
		self.label = QLabel(self)
		
		# loading image
		image = Image.open('NoSignal.png')
		self.pixmap = ImageQt.toqpixmap(image)
		self.label.resize(self.windowWidth, self.windowHeight)
	    # adding image to label
		self.label.setPixmap(self.pixmap.scaled(self.label.width(), self.label.height(), aspectRatioMode=Qt.IgnoreAspectRatio)) #,Qt::KeepAspectRatio)
		# self.label.setScaledContents(True)
        # QEvent.Resize.Connect(OnResize)
		# Optional, resize label to image size


		# show all the widgets
		self.show()

# create pyqt5 app
App = QApplication(sys.argv)

# create the instance of our Window
window = Window()

# start the app
sys.exit(App.exec())
