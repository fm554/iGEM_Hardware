import serial
import time

# Open serial port (replace 'COM3' with your Arduino's port)
ser = serial.Serial('COM4', 9600)
time.sleep(2)  # Wait for Arduino to reset

# JSON test data to send
json_data = '{"state": 1, "m_mode": 1, "pol": 1, "pwr": 100, "freq": 1.01}\n'

# Send JSON data to Arduino
ser.write(json_data.encode('utf-8'))

# Wait for Arduino to respond and read the response
time.sleep(1)
while ser.in_waiting > 0:
    print(ser.readline().decode('utf-8').strip())

# Close the serial port
ser.close()
