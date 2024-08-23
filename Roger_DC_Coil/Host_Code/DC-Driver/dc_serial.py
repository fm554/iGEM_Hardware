import serial
import time
import serial.tools.list_ports
import asyncio


class SerialConnection:
    def __init__(self,port_name, baud_rate=115200, timeout=0.1):
        self.port_name = port_name
        self.baud_rate = baud_rate
        self.timeout = timeout
        self.ser = None
        self.ser
    
    def alive(self):
        return self.ser.is_open

def list_serial_ports():
    """ Lists all available serial ports """
    ports = serial.tools.list_ports.comports()
    return [port.device for port in ports]

def open_serial_port(port_name, baud_rate=9600, timeout=1):
    """ Opens a serial port """
    try:
        ser = serial.Serial(port_name, baud_rate, timeout=timeout)
        #print(f"Opened port {port_name} successfully.")
        return ser
    except serial.SerialException as e:
        print(f"Error opening serial port {port_name}: {e}")
        return None

def close_serial_port(ser):
    """ Closes the serial port """
    if ser and ser.is_open:
        ser.close()
        print("Closed serial port successfully.")

def write_read(ser,x):
    ser.write(bytes(x,  'ascii'))
    #print(f'Sent: {x}'.encode('UTF-8'))
    time.sleep(0.05)
    data = ser.readline()
    return  data.decode('ascii')

def calculate_even_parity(string):
    count = 0
    for char in string:
        count += bin(ord(char)).count('1')
    return count % 2 == 0

def validate_checksum(self, param_string):
    params = param_string.split(";")
    if len(params) == 6:
        on = int(params[0])
        mode = int(params[1])
        pole = int(params[2])
        amplitude = int(float(params[3]))
        freq = int(float(params[4]))
        checksum = int(params[5])
        calculated_parity = calculate_even_parity(param_string)
        return [calculated_parity == checksum, calculated_parity]
    else:
        return [False, None]
    
if __name__ == "__main__":
    serial_ports = list_serial_ports()
    print(f"Available serial ports: {serial_ports}")
    port_name = input("Enter the port name: ")
    ser = open_serial_port(port_name)
    while True:
        num = input("Enter a number: ")
        value  = write_read(ser,num)
        print(value)