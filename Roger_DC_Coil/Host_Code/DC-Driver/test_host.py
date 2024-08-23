import serial
import time

def main():
    port = 'COM1'  # Use the other end of the virtual COM port pair
    baud_rate = 9600

    try:
        ser = serial.Serial(port, baud_rate, timeout=1)
        print(f"Opened port {port} successfully.")
    except serial.SerialException as e:
        print(f"Error opening serial port {port}: {e}")
        return

    try:
        while True:
            ser.write(b'PING\n')
            print('Sent: PING')
            response = ser.readline().decode('utf-8').strip()
            if response:
                print(f'Received: {response}')
            time.sleep(2)
    except KeyboardInterrupt:
        print("Stopping serial communication.")
    finally:
        ser.close()

if __name__ == "__main__":
    main()
