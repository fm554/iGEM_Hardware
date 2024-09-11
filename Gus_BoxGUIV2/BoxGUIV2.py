import sys
from PyQt6.QtWidgets import QMainWindow, QApplication, QPushButton, QCheckBox, QWidget, QCheckBox, QTabWidget,QVBoxLayout, QHBoxLayout, QLabel, QTextEdit, QFrame, QGridLayout, QLineEdit
from PyQt6.QtGui import QIcon, QPixmap, QImage, QFont, QTextCursor
from PyQt6 import QtCore
from PyQt6.QtCore import pyqtSlot, QTimer, Qt, QThread, pyqtSignal
import PyQt6.QtWidgets
from PIL import Image, ImageQt
import PyQt6
import gpiod
from magenta_lib import img_mode

import picamera2

import subprocess
import time
import serial

white_GPIO = 23
blue_GPIO = 24
chip = gpiod.Chip('gpiochip0')
global white_line
white_line = chip.get_line(white_GPIO)
white_line.request(consumer="LED", type=gpiod.LINE_REQ_DIR_OUT)
global blue_line
blue_line = chip.get_line(blue_GPIO)
blue_line.request(consumer="LED", type=gpiod.LINE_REQ_DIR_OUT)

global serial_port
serial_port=serial.Serial('/dev/ttyUSB0', 9600, timeout=1)

class App(QMainWindow):
	def __init__(self):
		super().__init__()
		self.title = 'MagentaBase (V1)'
		self.left = 200
		self.top = 200
		self.width = 800    
		self.height = 600
		self.setWindowTitle(self.title)
		self.setGeometry(self.left, self.top, self.width, self.height)
		# self.setMinimumHeight(self.height)
		# self.setMinimumWidth(800)
		# self.setMaximumWidth(800)
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
		vlayout.addWidget(self.tab_widget)

		self.textbox = QTextEdit(self)
		self.text_update.connect(self.append_text)
		sys.stdout = self
		print("Started Up")

		vlayout.addWidget(self.textbox)
		vlayout.addStretch()
		self.setLayout(vlayout)

		self.tab_widget.Imaging.capture_img.connect(self.cameras_widget.camera_widget.on_shutter)
		self.tab_widget.Imaging.capture_thermal.connect(self.cameras_widget.thermal_cam.on_shutter)

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
		self.missed_frames.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

		cam_labels_hlayout.addWidget(self.missed_frames)

		cam_vlayout.addLayout(cam_labels_hlayout)
		self.camera_widget = CameraWidget(self)

		self.camera_widget.frame_miss_count.connect(self.update_label)
		cam_vlayout.addWidget(self.camera_widget)

		thermal_vlayout = QVBoxLayout()
		thermal_labels_hlayout = QHBoxLayout()
		thermal_labels_hlayout.addWidget(QLabel("<b>Thermal Camera:</b>"))
		self.thermal_missed_frames = QLabel("Missed Frames: ???")
		self.thermal_missed_frames.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
		thermal_labels_hlayout.addWidget(self.thermal_missed_frames)

		thermal_vlayout.addLayout(thermal_labels_hlayout)
		self.thermal_cam = ThermalWidget(self)
		thermal_vlayout.addWidget(self.thermal_cam)
		hlayout.addLayout(cam_vlayout)
		hlayout.addLayout(thermal_vlayout)
		self.thermal_cam.thermal_frame_miss_count.connect(self.update_thermal_label)
		self.setLayout(hlayout)

			# camera_widget = CameraWidget()
		# layout.addWidget(camera_widget)

	@pyqtSlot(int)
	def update_label(self, count):
		self.missed_frames.setText("Missed Frames: " + str(count))
	
	@pyqtSlot(int)
	def update_thermal_label(self, count):
		self.thermal_missed_frames.setText("Missed Frames: " + str(count))

class CameraFrameCapture(QThread):
	frame_captured = pyqtSignal(object)
	frame_missed = pyqtSignal(object)
	def __init__(self, camera, shutter, parent):
		QThread.__init__(self, parent)
		self.camera = camera
	def run(self):
		try:
			image = self.camera.capture_image()
			image = image.convert("RGBA")
			
			data = image.tobytes("raw", "RGBA")
			qim = ImageQt.ImageQt(image)
			pix = PyQt6.QtGui.QPixmap.fromImage(qim)


			self.frame_missed.emit(0)
			self.frame_captured.emit(pix)

		except:
			image = Image.open('NoSignal.png')
			pix = ImageQt.toqpixmap(image)
			self.frame_missed.emit(1)
			self.frame_captured.emit(pix)

class CameraWidget(QWidget):
	frame_miss_count = pyqtSignal(int)
	def __init__(self, parent):
		super(CameraWidget, self).__init__(parent)
		self.missed_frames_count = 0
		self.savenext = False
		self.savename = ""
		try:
			self.camera = picamera2.Picamera2()
			self.camera.sensor_mode = 2  # Choose sensor mode 2 for 640x480 resolution
			self.camera.configure(self.camera.create_preview_configuration(main={"size": (640, 480)}))
			self.camera.start()
		except:
			self.camera = 0
		self.label = QLabel()
		# self.label.setMinimumSize(0, 0)
		self.label.resize(500, 300)
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
		frame_capture_thread = CameraFrameCapture(self.camera, self.savenext, parent=self)
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
		# self.label.setPixmap(pix)
		# self.label.setMinimumSize(0, 0)
		if self.savenext:
			pix.save(("./Captures/"+self.savename+".png"))
			print("Saved: " + "./Captures/"+self.savename+".png")
			self.savenext = False
		
		self.label.setPixmap(pix.scaled(self.label.width(), self.label.height(), aspectRatioMode=Qt.AspectRatioMode.KeepAspectRatio))

	@pyqtSlot(str)
	def on_shutter(self, name):
		self.savenext = True
		self.savename = name

class ThermalFrameCapture(QThread):
	thermal_frame_captured = pyqtSignal(object)
	thermal_frame_missed = pyqtSignal(object)
	def __init__(self, parent):
		QThread.__init__(self, parent)
		
	def run(self):
		try:
			with subprocess.Popen(["sudo", "./Gus_BoxGUIV2/rawrgb", "{}".format(8)], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE) as therm_camera:
				frame1 = therm_camera.stdout.read(2304)
				time.sleep(1.0 / 8.0)

				frame2 = therm_camera.stdout.read(2304)
				time.sleep(1.0 / 8.0)

				frame3 = therm_camera.stdout.read(2304)
				time.sleep(1.0 / 8.0)


				image = Image.frombytes('RGB', (32, 24), frame3)
						
				qim = ImageQt.ImageQt(image)
				pix = PyQt6.QtGui.QPixmap.fromImage(qim)

				self.thermal_frame_missed.emit(0)
				self.thermal_frame_captured.emit(pix)

		except:
			image = Image.open('NoSignal.png')
			pix = ImageQt.toqpixmap(image)
			self.thermal_frame_missed.emit(1)
			self.thermal_frame_captured.emit(pix)

class ThermalWidget(QWidget):
	thermal_frame_miss_count = pyqtSignal(int)
	def __init__(self, parent):
		super(ThermalWidget, self).__init__(parent)
		self.missed_frames_count = 0
		self.savename = ""
		self.savenext = False

		self.label = QLabel()
		# self.label.setMinimumSize(0, 0)
		self.label.resize(500, 500)
		image = Image.open('NoSignal.png')
		self.pixmap = ImageQt.toqpixmap(image)
		self.label.setPixmap(self.pixmap.scaled(self.label.width(), self.label.height(), aspectRatioMode=Qt.AspectRatioMode.KeepAspectRatio))
		self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
		layout = QHBoxLayout()
		layout.addWidget(self.label)
		self.setLayout(layout)

		self.timer = QTimer()
		self.timer.timeout.connect(self.start_capture)
		self.timer.start(int(1000/2))

	def start_capture(self):
		thermal_frame_capture_thread = ThermalFrameCapture(parent=self)
		thermal_frame_capture_thread.thermal_frame_captured.connect(self.on_frame_ready)
		thermal_frame_capture_thread.thermal_frame_missed.connect(self.update_missed)
		thermal_frame_capture_thread.start()

	@pyqtSlot(object)
	def update_missed(self, val):
		if val == 0:
			self.missed_frames_count = 0
		if val == 1:
			self.missed_frames_count += 1
		self.thermal_frame_miss_count.emit(self.missed_frames_count)

	@pyqtSlot(object)
	def on_frame_ready(self, pix):
		# self.label.setPixmap(pix)
		# self.label.setMinimumSize(0, 0)
		if self.savenext:
			pix.save(("./Captures/"+self.savename+".png"))
			print("Saved: " + "./Captures/"+self.savename+".png")
			self.savenext = False
		self.label.setPixmap(pix.scaled(self.label.width(), self.label.height(), aspectRatioMode=Qt.AspectRatioMode.KeepAspectRatio))
	
	@pyqtSlot(str)
	def on_shutter(self,name):
		self.savenext=True
		self.savename=name

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

		imaging_mode_layout = QHBoxLayout()

		self.light_switch = QCheckBox(text="Lights On")
		self.light_switch.stateChanged.connect(self.on_lights_on)
		self.fluoro_toggle = QCheckBox(text="Fluoresent Mode")
		self.fluoro_toggle.stateChanged.connect(self.on_fluoro_toggle)
		self.fluoro_toggle.setEnabled(False)

		imaging_mode_layout.addWidget(self.light_switch)
		imaging_mode_layout.addWidget(self.fluoro_toggle)

		coil_energise_layout = QHBoxLayout()
		self.energise_x = QCheckBox(text="Energise X-Coil")
		self.energise_y = QCheckBox(text="Energise Y-Coil")
		
		self.energise_x.stateChanged.connect(self.on_energise_x)
		self.energise_y.stateChanged.connect(self.on_energise_y)
	
		coil_energise_layout.addWidget(self.energise_x)
		coil_energise_layout.addWidget(self.energise_y)

		# right_layout.addWidget(QLabel("<b>Imaging Mode:<\b>"))
		# right_layout.addLayout(imaging_mode_layout)
		# right_layout.addWidget(QLabel("<b>Coils:<\b>"))
		# right_layout.addLayout(coil_energise_layout)
		# right_layout.setContentsMargins(0, 0, 0, 0)
		# right_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
		# right_frame.setLayout(right_layout)


		# left_layout = QVBoxLayout()
		# left_layout.addWidget(QLabel("<b>X Motor:<\b>"))
		
		XButtons_layout = QHBoxLayout()
		self.XCalibrate = QPushButton()
		self.XCalibrate.setText("Calibrate")
		self.XCalibrate.pressed.connect(self.on_xcalibrate)
		self.X0 = QPushButton()
		self.X0.setText("Zero")
		self.X0.pressed.connect(self.on_x0)
		self.XCentre = QPushButton()
		self.XCentre.setText("Centre")
		self.XCentre.pressed.connect(self.on_xcentre)
		
		XButtons_layout.addWidget(self.XCalibrate)
		XButtons_layout.addWidget(self.X0)
		XButtons_layout.addWidget(self.XCentre)
		
		# left_layout.addLayout(XButtons_layout)
		# left_layout.addWidget(QLabel("<b>Y Motor:<\b>"))

		YButtons_layout = QHBoxLayout()
		self.YCalibrate = QPushButton()
		self.YCalibrate.setText("Calibrate")
		self.YCalibrate.pressed.connect(self.on_ycalibrate)
		self.Y0 = QPushButton()
		self.Y0.setText("Zero")
		self.Y0.pressed.connect(self.on_y0)
		self.YCentre = QPushButton()
		self.YCentre.setText("Centre")
		self.YCentre.pressed.connect(self.on_ycentre)
		
		YButtons_layout.addWidget(self.YCalibrate)
		YButtons_layout.addWidget(self.Y0)
		YButtons_layout.addWidget(self.YCentre)
		# left_layout.addLayout(YButtons_layout)

		
		# rl_layout = QHBoxLayout()
		# rl_layout.addWidget(right_frame)
		# rl_layout.addLayout(left_layout)
		# rl_layout.setContentsMargins(10, 10, 10, 10)

		# ovl_frame  = QFrame()
		# ovl_frame.setFrameShape(QFrame.Shape.VLine)
		# ovl_frame.setLayout(rl_layout)

		# ovl = QHBoxLayout()
		# ovl.addWidget(ovl_frame)

		overall_layout = QGridLayout()
		overall_layout.addWidget(QLabel("<b>Imaging Mode:<\b>"), 0, 0)
		overall_layout.addLayout(imaging_mode_layout, 1, 0)
		overall_layout.addWidget(QLabel("<b>Coils:<\b>"), 2, 0)
		overall_layout.addLayout(coil_energise_layout, 3, 0)

		overall_layout.addWidget(QLabel("<b>X Motor:<\b>"), 0, 1)
		overall_layout.addLayout(XButtons_layout, 1, 1)
		overall_layout.addWidget(QLabel("<b>Y Motor:<\b>"), 2, 1)
		overall_layout.addLayout(YButtons_layout, 3, 1)
		self.setLayout(overall_layout)
	
	@pyqtSlot()
	def on_lights_on(self):
		if self.light_switch.isChecked():
			self.fluoro_toggle.setEnabled(True)
			if self.fluoro_toggle.isChecked():
				print("On: Fluorescent")
				img_mode(serial_port, 2, white_line, blue_line)
			else:
				print("On: Standard")
				img_mode(serial_port, 1, white_line, blue_line)
		else:
			self.fluoro_toggle.setEnabled(False)
			print("Off")
			img_mode(serial_port, 0, white_line, blue_line)
	
	@pyqtSlot()
	def on_fluoro_toggle(self):
		if self.fluoro_toggle.isChecked():
			print("On: Fluorescent")
			img_mode(serial_port, 2, white_line, blue_line)
			# turn on blue light
			# change servo angle
		else:
			print("On: Standard")
			img_mode(serial_port, 1, white_line, blue_line)

	@pyqtSlot()
	def on_energise_x(self):
		if self.energise_x.isChecked():
			print("On: X Coil")
			self.energise_y.setEnabled(False)
		else:
			print("Off: X Coil")
			self.energise_y.setEnabled(True)

	@pyqtSlot()
	def on_energise_y(self):
		if self.energise_y.isChecked():
			print("On: Y Coil")
			self.energise_x.setEnabled(False)
		else:
			print("Off: Y Coil")
			self.energise_x.setEnabled(True)

	@pyqtSlot()
	def on_xcalibrate(self):
		print("X Stage: calibrate")
		self.YCentre.setEnabled(True)	

	@pyqtSlot()
	def on_x0(self):
		print("X Stage: 0")
		self.YCentre.setEnabled(True)
	
	@pyqtSlot()
	def on_xcentre(self):
		print("X Stag: centre")
		self.YCentre.setEnabled(False)

	@pyqtSlot()
	def on_ycalibrate(self):
		print("Y Stage: calibrate")
		self.XCentre.setEnabled(True)	

	@pyqtSlot()
	def on_y0(self):
		print("Y Stage: 0")
		self.XCentre.setEnabled(True)
	
	@pyqtSlot()
	def on_ycentre(self):
		print("Y Stage: centre")
		self.XCentre.setEnabled(False)
	
class ImagingTab(QWidget):
	capture_img = pyqtSignal(str)
	capture_thermal = pyqtSignal(str)
	def __init__(self, parent):
		super(QWidget, self).__init__(parent)

		hlayout  = QHBoxLayout()

		r_layout = QVBoxLayout()
		r_file_layout = QHBoxLayout()
		r_layout.addWidget(QLabel("<b>Image<\b>"))
		r_file_layout.addWidget(QLabel("File Name:"))
		self.cam_file_namebox = QLineEdit()
		r_file_layout.addWidget(self.cam_file_namebox)
		r_layout.addLayout(r_file_layout)

		self.cam_capture = QPushButton()
		self.cam_capture.setText("Capture")
		r_layout.addWidget(self.cam_capture)
		r_layout.addStretch()
		l_layout = QVBoxLayout()
		l_file_layout = QHBoxLayout()
		l_layout.addWidget(QLabel("<b>Thermal Image<\b>"))
		l_file_layout.addWidget(QLabel("File Name:"))
		self.therm_file_namebox = QLineEdit()
		l_file_layout.addWidget(self.therm_file_namebox)
		l_layout.addLayout(l_file_layout)

		self.therm_capture = QPushButton()
		self.therm_capture.setText("Capture")
		l_layout.addWidget(self.therm_capture)
		l_layout.addStretch()
		hlayout.addLayout(r_layout)
		hlayout.addLayout(l_layout)

		self.setLayout(hlayout)

		#logic
		self.cam_capture.clicked.connect(self.on_cam_capture)
		self.therm_capture.clicked.connect(self.on_therm_capture)


	@pyqtSlot()
	def on_cam_capture(self):
		print("Photo")
		self.capture_img.emit(self.cam_file_namebox.text())
	def on_therm_capture(self):
		print("Capture")
		self.capture_thermal.emit(self.therm_file_namebox.text())	

class ProtocolsTab(QWidget):
	def __init__(self, parent):
		super(QWidget, self).__init__(parent)
		#support for up to 6 protocols
		self.p1 = QPushButton()
		self.p1.setText("P1")
		self.p2 = QPushButton()
		self.p2.setText("P2")
		self.p3 = QPushButton()
		self.p3.setText("P3")
		self.p4 = QPushButton()
		self.p4.setText("P4")
		self.p5 = QPushButton()
		self.p5.setText("P5")
		self.p6 = QPushButton()
		self.p6.setText("P6")

		self.cancel = QPushButton()
		self.cancel.setText("Cancel")
		self.cancel.setStyleSheet("background-color : red")

		grid_layout = QGridLayout()
		grid_layout.addWidget(self.p1, 0, 0)
		grid_layout.addWidget(self.p2, 0, 1)
		grid_layout.addWidget(self.p3, 0, 2)
		grid_layout.addWidget(self.p4, 1, 0)
		grid_layout.addWidget(self.p5, 1, 1)
		grid_layout.addWidget(self.p6, 1, 2)
		grid_layout.addWidget(self.cancel, 2, 2)

		self.setLayout(grid_layout)

		self.disable()

	def disable(self):
		self.p1.setEnabled(False)
		self.p2.setEnabled(False)
		self.p3.setEnabled(False)
		self.p4.setEnabled(False)
		self.p5.setEnabled(False)
		self.p6.setEnabled(False)
		
	
if __name__ == '__main__':
	app = QApplication(sys.argv)
	ex = App()
	sys.exit(app.exec())
