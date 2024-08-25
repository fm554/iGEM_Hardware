from PyQt5.QtWidgets import (
    QApplication, QWidget, QPushButton, QVBoxLayout, QHBoxLayout,
    QLabel, QComboBox, QLineEdit, QRadioButton, QGridLayout
)
import sys
import quick_serial
import asyncio
import threading

import json

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
        self.refresh_button = QPushButton("Refresh")
        self.refresh_button.setFixedSize(100, 50)
        self.connect_button = QPushButton("Connect")  # Added connect button
        serial_layout.addWidget(self.serial_label)
        serial_layout.addWidget(self.serial_combo)
        serial_layout.addWidget(self.refresh_button)
        serial_layout.addWidget(self.connect_button)  # Added connect button
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

        # power Entry
        power_layout = QHBoxLayout()
        self.power_label = QLabel("power")
        self.power_entry = QLineEdit()
        power_layout.addWidget(self.power_label)
        power_layout.addWidget(self.power_entry)
        layout.addLayout(power_layout)

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
        self.dc_button.clicked.connect(self.set_dc_mode)
        self.ac_button.clicked.connect(self.set_ac_mode)
        self.n_button.clicked.connect(self.set_n_pole)
        self.s_button.clicked.connect(self.set_s_pole)
        self.freq_entry.returnPressed.connect(lambda: self.set_freq(float(self.freq_entry.text())))
        self.freq_01_button.clicked.connect(lambda: self.set_freq(0.1))
        self.freq_1_button.clicked.connect(lambda: self.set_freq(1))
        self.freq_10_button.clicked.connect(lambda: self.set_freq(10))
        self.power_entry.returnPressed.connect(lambda: self.set_power(float(self.power_entry.text())))
        self.power_25_button.clicked.connect(lambda: self.set_power(25))
        self.power_50_button.clicked.connect(lambda: self.set_power(50))
        self.power_75_button.clicked.connect(lambda: self.set_power(75))
        self.power_100_button.clicked.connect(lambda: self.set_power(100))
        self.on_button.clicked.connect(self.turn_on)
        self.off_button.clicked.connect(self.turn_off)
        self.refresh_button.clicked.connect(self.update_port_list)
        self.connect_button.clicked.connect(self.connect_magnet)

    def parameter_init(self):
        self.state = 0  # 0:off, 1:on
        self.mode = 0  # 0: DC, 1: AC
        self.pole = 0  # 0: N, 1: S
        self.power = 0  # power
        self.freq = 0  # frequency
        self.status = "Not_Connected"

    def set_dc_mode(self):
        self.ac_button.setStyleSheet("")
        self.dc_button.setStyleSheet("background-color: lightblue")
        self.mode = 0
        self.disable_ac_controls()
        self.turn_off()

    def set_ac_mode(self):
        self.dc_button.setStyleSheet("")
        self.ac_button.setStyleSheet("background-color: lightblue")
        self.mode = 1
        self.enable_ac_controls()
        self.turn_off()

    def set_n_pole(self):
        if self.mode == 0:
            self.n_button.setStyleSheet("background-color: lightblue")
            self.s_button.setStyleSheet("")
            self.pole = 0
            self.turn_off()

    def set_s_pole(self):
        if self.mode == 0:
            self.s_button.setStyleSheet("background-color: lightblue")
            self.n_button.setStyleSheet("")
            self.pole = 1
            self.turn_off()

    def set_freq(self, freq):
        if self.mode == 0:
            return
        self.freq_entry.setText(str(freq))
        self.update_freq_buttons(freq)
        self.freq = float(freq)

    def set_power(self, power):
        self.power_entry.setText(str(power))
        self.update_power_buttons(power)
        self.power = float(power)

    def turn_on(self):
        self.on_button.setStyleSheet("background-color: green")
        self.off_button.setStyleSheet("")
        self.state = 1

    def turn_off(self):
        self.on_button.setStyleSheet("")
        self.off_button.setStyleSheet("background-color: red")
        self.state = 0

    def update_port_list(self):
        ports = quick_serial.list_serial_ports()
        self.serial_combo.clear()
        self.serial_combo.addItems(ports)
        if self.serial_combo.currentText() not in ports:
            self.set_status("Disconnected")
    

    def get_param(self):
        if self.mode != "NA":
            # Create a dictionary with the parameters
            params = {
                "state": self.state,
                "m_mode": self.mode,
                "pol": self.pole,
                "pwr": self.power,
                "freq": self.freq
            }
            
            # Serialize the dictionary to a JSON string
            param_json = json.dumps(params)
            return param_json
        else:
            return "NA"


    def connect_magnet(self):
        port = self.serial_combo.currentText()
        self.ser = quick_serial.start_serial(port)
        if self.ser:
            self.set_status("Connected")
            self.loop = asyncio.new_event_loop()
            threading.Thread(target=self.start_loop, args=(self.loop,)).start()
            asyncio.run_coroutine_threadsafe(self.update_magnet_loop(), self.loop)
        else:
            self.set_status("Connection Failed")

    def start_loop(self, loop):
        asyncio.set_event_loop(loop)
        loop.run_forever()

    async def update_magnet_loop(self):
        while True:
            self.update_magnet()
            #print("Updated")
            await asyncio.sleep(0.2)

    
    def update_magnet(self):
        param = self.get_param()
        if param != "NA":
            print(param)
            value = quick_serial.write_read(self.ser, param)
            print(value)
            if value != "READOK":
                #print(value)
                self.set_status("Err Connecting")
        else:
            self.set_status("Invalid Parameters")

    def set_status(self, status):
        self.status_label.setText(status)

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

    def disable_ac_controls(self):
        self.freq_label.setStyleSheet("background-color: lightgrey")
        self.freq_entry.setStyleSheet("background-color: lightgrey")
        self.freq_01_button.setStyleSheet("background-color: lightgrey")
        self.freq_1_button.setStyleSheet("background-color: lightgrey")
        self.freq_10_button.setStyleSheet("background-color: lightgrey")
        self.n_button.setStyleSheet("")
        self.s_button.setStyleSheet("")

    def enable_ac_controls(self):
        self.freq_label.setStyleSheet("")
        self.freq_entry.setStyleSheet("")
        self.freq_01_button.setStyleSheet("")
        self.freq_1_button.setStyleSheet("")
        self.freq_10_button.setStyleSheet("")
        self.n_button.setStyleSheet("background-color: lightgrey")
        self.s_button.setStyleSheet("background-color: lightgrey")

    def update_freq_buttons(self, freq):
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

    def update_power_buttons(self, power):
        switcher = {
            25: self.power_25_button,
            50: self.power_50_button,
            75: self.power_75_button,
            100: self.power_100_button
        }
        for value, button in switcher.items():
            if value == power:
                button.setChecked(True)
                button.setStyleSheet("background-color: lightblue")
            else:
                button.setChecked(False)
                button.setStyleSheet("")

class DropdownSerial(QComboBox):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent

    def focusOutEvent(self, event):
        super().focusOutEvent(event)
        control_panel.update_port_list()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    control_panel = ControlPanel()
    control_panel.show()
    sys.exit(app.exec_())
