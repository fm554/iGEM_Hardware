import sys
from PyQt6.QtWidgets import QMainWindow, QApplication, QPushButton, QWidget, QCheckBox, QTabWidget,QVBoxLayout, QHBoxLayout, QLabel, QTextEdit
from PyQt6.QtGui import QIcon, QPixmap, QImage, QFont, QTextCursor
from PyQt6 import QtCore
from PyQt6.QtCore import pyqtSlot, QTimer, Qt, QThread, pyqtSignal
from qtwidgets import Toggle
from PIL import Image, ImageQt

import PyQt6
try:
	import PIL.ImageTk
	import picamera2
except:
	print("No RPI")

class App(QMainWindow):
	def __init__(self):
		super().__init__()
		self.title = 'MagentaBase (V1)'
		self.left = 200
		self.top = 200
		self.width = 400    
		self.height = 600
		self.setWindowTitle(self.title)
		self.setGeometry(self.left, self.top, self.width, self.height)
		
		self.setCentralWidget(OverallView(self))
	
		self.show()

class OverallView(QWidget):
	text_update = pyqtSignal(str)
	def __init__(self, parent):
		super(QWidget, self).__init__(parent)

		vlayout = QVBoxLayout()

		#cameras_widget
		self.cameras_widget = CameraView(self)
		vlayout.addWidget(self.cameras_widget)


		self.tab_widget = TabLayout(self)
		self.tab_widget.setMinimumHeight(200)
		self.tab_widget.resize(parent.width,200)
		vlayout.addWidget(self.tab_widget)

		self.textbox = QTextEdit(self)
		self.textbox.resize(parent.width, 100)
		self.textbox.setMinimumHeight(100)
		self.text_update.connect(self.append_text)
		sys.stdout = self
		print("Started Up")

		# vlayout.addWidget(self.cam_widget)
	
		vlayout.addWidget(self.textbox)
		self.setLayout(vlayout)
		# vlayout.addWidget(self.textbox)

	def write(self, text):
		self.text_update.emit(str(text))
	def flush(self):
		pass
	
	# Append to text display
	def append_text(self, text):
		cur = self.textbox.textCursor()     # Move cursor to end of text
		cur.movePosition(QTextCursor.MoveOperation.End) 
		s = str(text)
		while s:
			head,sep,s = s.partition("\n")  # Split line at LF
			cur.insertText(head)            # Insert text at cursor
			if sep:                         # New line if LF
				cur.insertBlock()
		self.textbox.setTextCursor(cur) 

class CameraView(QWidget):
	def __init__(self, parent):
		
		super(QWidget, self).__init__(parent)

		hlayout = QHBoxLayout()
		
		cam_vlayout = QVBoxLayout()
		cam_labels_hlayout = QHBoxLayout()

		cam_labels_hlayout.addWidget(QLabel("<b>Camera:</b>"))
		self.missed_frames = QLabel("Missed Frames: ???")
		self.missed_frames.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight)

		cam_labels_hlayout.addWidget(self.missed_frames)

		cam_vlayout.addLayout(cam_labels_hlayout)
		self.camera_widget = CameraWidget(self)

		self.camera_widget.frame_miss_count.connect(self.update_label)
		cam_vlayout.addWidget(self.camera_widget)

		hlayout.addLayout(cam_vlayout)
		#hlayout.addWidget(self.camera_widget)

		self.setLayout(hlayout)

			# camera_widget = CameraWidget()
		# layout.addWidget(camera_widget)

	@pyqtSlot(int)
	def update_label(self, count):
		self.missed_frames.setText("Missed Frames: " + str(count))

class CameraFrameCapture(QThread):
	frame_captured = pyqtSignal(object)
	frame_missed = pyqtSignal(object)
	def __init__(self, camera, parent):
		QThread.__init__(self, parent)
		self.camera = camera
	def run(self):
# 		try:
		image = self.camera.capture_image()
		image = image.convert("RGBA")
		data = image.tobytes("raw", "RGBA")
		qim = ImageQt.ImageQt(image)
		pix = PyQt6.QtGui.QPixmap.fromImage(qim)

		self.frame_missed.emit(0)
		self.frame_captured.emit(pix)

# 		except:
# 			image = Image.open('NoSignal.png')
# 			pix = ImageQt.toqpixmap(image)
# 			self.frame_missed.emit(1)
# 			self.frame_captured.emit(pix)

class CameraWidget(QWidget):
	frame_miss_count = pyqtSignal(int)
	def __init__(self, parent):
		super(CameraWidget, self).__init__(parent)
		self.missed_frames_count = 0
		try:
			self.camera = picamera2.Picamera2()
			self.camera.sensor_mode = 2  # Choose sensor mode 2 for 640x480 resolution
			self.camera.configure(self.camera.create_preview_configuration(main={"size": (640, 480)}))
			self.camera.start()
		except:
			pass

		self.label = QLabel()
		self.label.setMinimumSize(0, 0)
		#self.label.resize(400, 600)
		image = Image.open('NoSignal.png')
		self.pixmap = ImageQt.toqpixmap(image)
		self.label.setPixmap(self.pixmap.scaled(self.label.width(), self.label.height(), aspectRatioMode=Qt.AspectRatioMode.KeepAspectRatio))
		self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
		layout = QVBoxLayout()
		layout.addWidget(self.label)
		self.setLayout(layout)

		self.timer = QTimer()
		self.timer.timeout.connect(self.start_capture)
		self.timer.start(int(1000 / 5))

	def start_capture(self):
		frame_capture_thread = CameraFrameCapture(self.camera, parent=self)
		frame_capture_thread.frame_captured.connect(self.on_frame_ready)
		frame_capture_thread.frame_missed.connect(self.update_missed)
		frame_capture_thread.start()

	@pyqtSlot(object)
	def update_missed(self, val):
		if val == 0:
			self.missed_frames_count = 0
		if val == 1:
			self.missed_frames_count += 1
		self.frame_miss_count.emit(self.missed_frames_count)

	@pyqtSlot(object)
	def on_frame_ready(self, pix):
		#self.label.setPixmap(pix)
		# self.label.setMinimumSize(0, 0)
		self.label.setPixmap(pix.scaled(self.label.width(), self.label.height(), aspectRatioMode=Qt.AspectRatioMode.KeepAspectRatio))

class TabLayout(QWidget):
	
	def __init__(self, parent):
		super(QWidget, self).__init__(parent)
		overall_layout = QVBoxLayout()

		self.SystemTest = SystemTestTab(self)
		self.Imaging = ImagingTab(self)
		self.Protocols = ProtocolsTab(self)
		# Initialize tab screen
		self.tabs = QTabWidget()
		# self.tabs.resize(1000,800)

		# Add tabs
		self.tabs.addTab(self.SystemTest,"System Test")
		self.tabs.addTab(self.Imaging,"Imaging")
		self.tabs.addTab(self.Protocols, "Protocols")

		# Add tabs to widget
		overall_layout.addWidget(self.tabs)
		self.setLayout(overall_layout)

class SystemTestTab(QWidget):
	def __init__(self, parent):
		super(QWidget, self).__init__(parent)

		layout = QVBoxLayout()
		

		imaging_mode_layout = QHBoxLayout()
		self.light_switch = QCheckBox(text="Lights On")
		self.light_switch.stateChanged.connect(self.on_lights_on)
		self.fluoro_toggle = QCheckBox(text="Fluoresent Mode")
		self.fluoro_toggle.stateChanged.connect(self.on_fluoro_toggle)
		self.fluoro_toggle.setEnabled(False)

		imaging_mode_layout.addWidget(self.light_switch)
		imaging_mode_layout.addWidget(self.fluoro_toggle)

		coil_energise_layout = QHBoxLayout()
		self.energise_x = QCheckbox(text="Energise X-Coil")
		self.energise_y = QCheckbox(text"Energise Y-Coil")
		
		self.energise_x.stateChanged.connect(self.on_energise_x)
		self.energise_y.stateChanged.connect(self.on_energise_y)
		
		

		layout.addLayout(imaging_mode_layout)
		self.setLayout(layout)
	
	@pyqtSlot()
	def on_lights_on(self):
		if self.light_switch.isChecked():
			self.fluoro_toggle.setEnabled(True)
			if self.fluoro_toggle.isChecked():
				print("On: Fluorescent")
			else:
				print("On: Standard")
		else:
			self.fluoro_toggle.setEnabled(False)
			print("Off")
	
	@pyqtSlot()
	def on_fluoro_toggle(self):
		if self.fluoro_toggle.isChecked():
			print("On: Fluorescent")
			# turn on blue light
			# change servo angle
		else:
			print("On: Standard")

class ImagingTab(QWidget):
	def __init__(self, parent):
		super(QWidget, self).__init__(parent)
	#TODO

class ProtocolsTab(QWidget):
	def __init__(self, parent):
		super(QWidget, self).__init__(parent)
	#TODO
	
if __name__ == '__main__':
	app = QApplication(sys.argv)
	ex = App()
	sys.exit(app.exec())
