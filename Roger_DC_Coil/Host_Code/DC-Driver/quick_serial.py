import serial
import time
import serial.tools.list_ports
import logging

logging.basicConfig(level=logging.DEBUG)

def start_serial(port, baud_rate=9600, **kwargs):
    try:
        ser = serial.Serial(port, baud_rate, timeout=0.1, **kwargs)
        ser.xonxoff = True
        ser.stopbits = serial.STOPBITS_TWO
        print(f"Opened port {port} successfully.")
        return ser
    except serial.SerialException as e:
        print(f"Error opening serial port {port}: {e}")
        return None

def list_serial_ports():
    """ Lists all available serial ports """
    ports = serial.tools.list_ports.comports()
    return [port.device for port in ports]

def write_read(ser, x):
    try:
        ser.write(f"{x}\n".encode('latin-1'))  # Ensure a newline is sent
        time.sleep(0.1)
        data = b""
        while True:
            line = ser.readline()
            if not line:
                break
            data += line
        logging.debug(f"Received data: {data}")
        return data.decode('latin-1', errors='ignore').strip()
    except Exception as e:
        logging.error(f"Error during write/read: {e}")
        return ""

def close_serial(ser):
    if ser and ser.is_open:
        ser.close()
        print("Closed serial port successfully.")

if __name__ == "__main__":
    serial_ports = list_serial_ports()
    print(f"Available serial ports: {serial_ports}")
    port_name = input("Enter the port name: ")
    arduino = start_serial(port=port_name, baud_rate=115200)
    if not arduino:
        print("Exiting...")
        exit(1)
    print("Connected to Arduino successfully.")

    try:
        while True:
            num = input("Enter a number: ")
            value = write_read(arduino, num)
            print(f"Received: {value}")
    except KeyboardInterrupt:
        print("Exiting program...")
    finally:
        close_serial(arduino)
