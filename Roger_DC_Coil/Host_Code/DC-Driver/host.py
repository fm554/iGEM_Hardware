from PyQt5.QtWidgets import (
    QApplication, QWidget, QPushButton, QVBoxLayout, QHBoxLayout,
    QLabel, QComboBox, QLineEdit, QRadioButton, QGridLayout
)
from PyQt5.QtCore import Qt, QTimer
import sys
import asyncio
import serial
import time
import dc_serial

class ControlPanel(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Magnet Control")
        self.parameter_init()
        self.setup_ui()
        self.setup_connections()
        self.update_port_list()

    def setup_ui(self):
        layout = QVBoxLayout()

        # Serial Port Selector
        serial_layout = QHBoxLayout()
        self.serial_label = QLabel("Serial Port:")
        self.serial_combo = DropdownSerial()
        serial_layout.addWidget(self.serial_label)
        serial_layout.addWidget(self.serial_combo)

        # Refresh Button
        self.refresh_button = QPushButton("Refresh")
        self.refresh_button.setFixedSize(100, 50)  # Set the size of the button
        serial_layout.addWidget(self.refresh_button)
        layout.addLayout(serial_layout)

        # DC/AC Buttons
        dc_ac_layout = QHBoxLayout()
        self.dc_button = QPushButton("DC")
        self.ac_button = QPushButton("AC")
        dc_ac_layout.addWidget(self.dc_button)
        dc_ac_layout.addWidget(self.ac_button)
        layout.addLayout(dc_ac_layout)

        # N/S Buttons
        ns_layout = QHBoxLayout()
        self.n_button = QPushButton("N")
        self.s_button = QPushButton("S")
        ns_layout.addWidget(self.n_button)
        ns_layout.addWidget(self.s_button)
        layout.addLayout(ns_layout)

        # Frequency Setter
        freq_layout = QHBoxLayout()
        self.freq_label = QLabel("FREQ:")
        self.freq_entry = QLineEdit()
        freq_layout.addWidget(self.freq_label)
        freq_layout.addWidget(self.freq_entry)
        layout.addLayout(freq_layout)

        # Preset Frequency Buttons
        freq_buttons_layout = QHBoxLayout()
        self.freq_01_button = QPushButton("0.1 Hz")
        self.freq_1_button = QPushButton("1 Hz")
        self.freq_10_button = QPushButton("10 Hz")
        freq_buttons_layout.addWidget(self.freq_01_button)
        freq_buttons_layout.addWidget(self.freq_1_button)
        freq_buttons_layout.addWidget(self.freq_10_button)
        layout.addLayout(freq_buttons_layout)

        # Amplitude Entry
        amplitude_layout = QHBoxLayout()
        self.amplitude_label = QLabel("Amplitude")
        self.amplitude_entry = QLineEdit()
        amplitude_layout.addWidget(self.amplitude_label)
        amplitude_layout.addWidget(self.amplitude_entry)
        layout.addLayout(amplitude_layout)

        # Power Preset Buttons
        power_layout = QHBoxLayout()
        self.power_25_button = QRadioButton("25%")
        self.power_50_button = QRadioButton("50%")
        self.power_75_button = QRadioButton("75%")
        self.power_100_button = QRadioButton("100%")
        power_layout.addWidget(self.power_25_button)
        power_layout.addWidget(self.power_50_button)
        power_layout.addWidget(self.power_75_button)
        power_layout.addWidget(self.power_100_button)
        layout.addLayout(power_layout)

        # ON/OFF Buttons
        on_off_layout = QHBoxLayout()
        self.on_button = QPushButton("ON")
        self.on_button.setStyleSheet("background-color: green")
        self.off_button = QPushButton("OFF")
        on_off_layout.addWidget(self.on_button)
        on_off_layout.addWidget(self.off_button)
        layout.addLayout(on_off_layout)

        # Status Light Indicator
        self.status_label = QLabel("Status")
        layout.addWidget(self.status_label)

        self.setLayout(layout)

    def setup_connections(self):
        # Connect signals to functions
        self.dc_button.clicked.connect(self.set_dc_mode)
        self.ac_button.clicked.connect(self.set_ac_mode)
        self.n_button.clicked.connect(self.set_n_pole)
        self.s_button.clicked.connect(self.set_s_pole)
        self.freq_entry.returnPressed.connect(lambda: self.set_freq(float(self.freq_entry.text())))
        self.freq_01_button.clicked.connect(lambda: self.set_freq(0.1))
        self.freq_1_button.clicked.connect(lambda: self.set_freq(1))
        self.freq_10_button.clicked.connect(lambda: self.set_freq(10))
        self.amplitude_entry.returnPressed.connect(lambda: self.set_amplitude(float(self.amplitude_entry.text())))
        self.power_25_button.clicked.connect(lambda: self.set_amplitude(25))
        self.power_50_button.clicked.connect(lambda: self.set_amplitude(50))
        self.power_75_button.clicked.connect(lambda: self.set_amplitude(75))
        self.power_100_button.clicked.connect(lambda: self.set_amplitude(100))
        self.on_button.clicked.connect(self.turn_on)
        self.off_button.clicked.connect(self.turn_off)
        self.refresh_button.clicked.connect(self.update_port_list)

    def parameter_init(self):
        self.mode = "NA"  # DC or AC - "DC" or "AC"
        self.pole = "NA"  # Normal or Abnormal - "N" or "S"
        self.max_amplitude = 0  # to some mT
        self.amplitude = 0  # 0- max_amplitude
        self.freq = 0  # 0.01 - 100 Hz
        self.on = False
        self.status = "NORMAL"  # "NORMAL" or "ABNORMAL"

    def set_dc_mode(self):
        self.ac_button.setStyleSheet("")
        self.dc_button.setStyleSheet("background-color: lightblue")
        self.mode = "DC"
        self.freq_label.setStyleSheet("background-color: lightgrey")
        self.freq_entry.setStyleSheet("background-color: lightgrey")
        self.freq_01_button.setStyleSheet("background-color: lightgrey")
        self.freq_1_button.setStyleSheet("background-color: lightgrey")
        self.freq_10_button.setStyleSheet("background-color: lightgrey")
        self.n_button.setStyleSheet("")
        self.s_button.setStyleSheet("")
        self.turn_off()

    def set_ac_mode(self):
        self.dc_button.setStyleSheet("")
        self.ac_button.setStyleSheet("background-color: lightblue")
        self.mode = "AC"
        self.freq_label.setStyleSheet("")
        self.freq_entry.setStyleSheet("")
        self.freq_01_button.setStyleSheet("")
        self.freq_1_button.setStyleSheet("")
        self.freq_10_button.setStyleSheet("")
        self.n_button.setStyleSheet("background-color: lightgrey")
        self.s_button.setStyleSheet("background-color: lightgrey")
        self.turn_off()

    def set_n_pole(self):
        if self.mode == "DC":
            self.n_button.setStyleSheet("background-color: lightblue")
            self.s_button.setStyleSheet("")
            self.pole = "N"
            self.turn_off()

    def set_s_pole(self):
        if self.mode == "DC":
            self.s_button.setStyleSheet("background-color: lightblue")
            self.n_button.setStyleSheet("")
            self.pole = "S"
            self.turn_off()

    def set_freq(self, freq):
        if self.mode == "DC":
            return
        self.freq_entry.setText(str(freq))
        switcher = {
            0.1: self.freq_01_button,
            1: self.freq_1_button,
            10: self.freq_10_button
        }
        for value, button in switcher.items():
            if value == freq:
                button.setChecked(True)
                button.setStyleSheet("background-color: lightblue")
            else:
                button.setChecked(False)
                button.setStyleSheet("")
        self.freq = float(freq)

    def set_amplitude(self, amplitude):
        self.amplitude_entry.setText(str(amplitude))
        switcher = {
            25: self.power_25_button,
            50: self.power_50_button,
            75: self.power_75_button,
            100: self.power_100_button
        }
        for value, button in switcher.items():
            if value == amplitude:
                button.setChecked(True)
                button.setStyleSheet("background-color: lightblue")
            else:
                button.setChecked(False)
                button.setStyleSheet("")
        self.amplitude = float(amplitude)

    def turn_on(self):
        self.on_button.setStyleSheet("background-color: green")
        self.off_button.setStyleSheet("")
        self.on = True

    def turn_off(self):
        self.on_button.setStyleSheet("")
        self.off_button.setStyleSheet("background-color: red")
        self.on = False

    def update_port_list(self):
        ports = dc_serial.list_serial_ports()
        self.serial_combo.clear()
        self.serial_combo.addItems(ports)

    def get_param(self):
        if self.mode != "NA":
            on_value = 1 if self.on else 0
            mode_value = 1 if self.mode == "AC" else 0
            pole_value = 1 if self.pole == "N" else 0
            param_sum = f"{on_value};{mode_value};{pole_value};{self.amplitude};{self.freq};"
            checksum = dc_serial.calculate_even_parity(param_sum)
            return f"{param_sum}{checksum}"
        else:
            return "NA"

    def send_param(self):
        param = self.get_param()
        if param != "NA":
            dc_serial.send_param(param)

    def validate_checksum(self, param_string):
        params = param_string.split(";")
        if len(params) == 6:
            on = int(params[0])
            mode = int(params[1])
            pole = int(params[2])
            amplitude = int(float(params[3]))
            freq = int(float(params[4]))
            checksum = int(params[5])
            calculated_parity = dc_serial.calculate_even_parity(param_string)
            return [calculated_parity == checksum, calculated_parity]
        else:
            return [False, None]

    def show_param_window(self):
        self.param_window = QWidget()
        layout = QGridLayout()
        self.param_window.setLayout(layout)
        self.param_window.setWindowTitle("Parameters")
        self.param_window.setGeometry(100, 100, 200, 200)
        param_result = self.get_param()
        param_label = QLabel(param_result)
        layout.addWidget(param_label)
        if not self.validate_checksum(param_result)[0]:
            param_label.setStyleSheet("background-color: red; color: white; padding: 10px; font-weight: bold;")
            checksum_label = QLabel(str(self.validate_checksum(param_result)[1]))
            layout.addWidget(checksum_label)
        else:
            param_label.setStyleSheet("background-color: green; color: white; padding: 10px; font-weight: bold;")
        self.param_window.show()
        self.param_window.activateWindow()

class DropdownSerial(QComboBox):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent

    def focusOutEvent(self, event):
        super().focusOutEvent(event)
        control_panel.update_port_list()

class MagnetController:
    def __init__(self):
        self.control_panel = ControlPanel()
        self.control_panel.show()
        self.ONOFF = False
        self.POLE = "N"
        self.MODE = "DC"
        self.FREQ = 0.0
        self.INTERVAL = 0.0
        self.AMPLITUDE = 0.0
        self.PORT = ""
        sys.exit(app.exec_())

    def start(self):
        self.control_panel.show()
        sys.exit(app.exec_())

    def stop(self):
        sys.exit()

    def get_status(self):
        return self.control_panel.status

if __name__ == "__main__":
    app = QApplication(sys.argv)
    control_panel = ControlPanel()
    control_panel.show()
    sys.exit(app.exec_())
