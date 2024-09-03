import sys
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QPushButton, QAction, QLineEdit, QMessageBox, QLabel, qApp, QDesktopWidget
from PyQt5.QtGui import QIcon, QDesktopServices
from PyQt5.QtCore import pyqtSlot, Qt, QUrl, QTimer
from PIL import Image, ImageQt

class App(QMainWindow):

    def __init__(self): # the properties or whatever
        super().__init__()
        self.timer = QTimer()
        self.title = 'RandClick'
        self.left = 10
        self.top = 10
        self.windowWidth = 350
        self.windowHeight = 445
        self.initUI()

    def update(self):
        self.windowWidth = self.width() #update your width and height attributes to reflect the current width and height
        self.windowHeight = self.height()
        text = str(self.windowWidth) + ' , ' + str(self.windowHeight)
        self.l1.setText(text)

    def resizeEvent(self, event):
         self.update() #call your update method
         QtWidgets.QMainWindow.resizeEvent(self, event) #this line is present in the StackOverflow answer, but it seems to work without it for me, so YMMV

    def initUI(self): # the main bit of the program, like where they define the buttons or something
        self.setWindowTitle(self.title) # sets the window title to the title defined earlier
        self.setGeometry(self.left, self.top, self.windowWidth, self.windowHeight) # sets the window geometry to what was defined earlier
        # self.setWindowIcon(QtGui.QIcon('icon.png')) # sets the window icon
        
        text = str(self.windowWidth) + ' , ' + str(self.windowHeight)
        self.l1 = QLabel(text, self)
        self.l1.move(50, 50) # tells the program where the label should be
        
        self.l2 = QtWidgets.QLabel('Made by Thou', self) # tells itself that its a label, and also tells it what to say
        self.l2.setStyleSheet('color: #c1c1c1') # tells the program what color the label is
        self.l2.move(282, 414) # tells the program where the label should be

        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())        