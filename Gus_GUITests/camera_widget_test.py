import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QPixmap, QImage
import PIL.ImageTk
import picamera2

class CameraWidget(QWidget):
    def __init__(self, parent=None):
        super(CameraWidget, self).__init__(parent)

        self.camera = picamera2.Picamera2()
        self.camera.sensor_mode = 2  # Choose sensor mode 2 for 640x480 resolution
        self.camera.configure(self.camera.create_preview_configuration(main={"size": (640, 480)}))
        self.camera.start()

        self.label = QLabel()
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        self.setLayout(layout)

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(int(1000 / 24))

    def update_frame(self):
        image = self.camera.capture_array()
        qt_image = QImage(image.data, 640, 480, QImage.Format_RGB16)
        # qt_image = ImageQt(image).convertToQImage()
        pixmap = QPixmap.fromImage(qt_image)
        self.label.setPixmap(pixmap)

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.setWindowTitle("Raspberry Pi Camera Viewer")
        self.setGeometry(100, 100, 640, 480)

        self.central_widget = CameraWidget()
        self.setCentralWidget(self.central_widget)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())