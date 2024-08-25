import tkinter as tk
from tkinter import messagebox, scrolledtext
import serial
import json
import threading

# Initialize serial communication
def init_serial(port='COM3', baudrate=9600):
    try:
        ser = serial.Serial(port, baudrate, timeout=1)  # Set timeout to 1 second
        return ser
    except serial.SerialException as e:
        messagebox.showerror("Serial Port Error", f"Could not open port {port}: {e}")
        return None

# Function to send JSON data to serial port
def send_to_serial(ser, data):
    try:
        json_data = json.dumps(data)
        ser.write(json_data.encode('utf-8'))
        ser.write(b'\n ')  # Send newline to indicate end of message
        messagebox.showinfo("Success", "Data sent to serial port successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to send data: {e}")

# Function to collect data from input fields and send via serial
def send_data():
    state = bool(state_var.get())
    m_mode = bool(m_mode_var.get())
    pol = bool(pol_var.get())
    pwr = int(pwr_entry.get())
    freq = float(freq_entry.get())

    data = {
        "state": state,
        "m_mode": m_mode,
        "pol": pol,
        "pwr": pwr,
        "freq": freq
    }

    if serial_port:
        send_to_serial(serial_port, data)
    else:
        messagebox.showerror("Serial Port Error", "Serial port is not initialized.")

# Function to read data from serial port and display in the GUI
def read_serial():
    while True:
        if serial_port and serial_port.in_waiting > 0:
            response = serial_port.readline().decode('utf-8').strip()
            if response:
                response_text.insert(tk.END, response + '\n')
                response_text.yview(tk.END)  # Auto-scroll to the end

# Initialize the GUI window
root = tk.Tk()
root.title("Serial Data Sender")

# Create input fields for each parameter
tk.Label(root, text="State (0 or 1):").grid(row=0, column=0, padx=10, pady=5)
state_var = tk.IntVar()
tk.Radiobutton(root, text="OFF (0)", variable=state_var, value=0).grid(row=0, column=1)
tk.Radiobutton(root, text="ON (1)", variable=state_var, value=1).grid(row=0, column=2)

tk.Label(root, text="Magnet Mode (0 or 1):").grid(row=1, column=0, padx=10, pady=5)
m_mode_var = tk.IntVar()
tk.Radiobutton(root, text="DC (0)", variable=m_mode_var, value=0).grid(row=1, column=1)
tk.Radiobutton(root, text="AC (1)", variable=m_mode_var, value=1).grid(row=1, column=2)

tk.Label(root, text="Polarity (0 or 1):").grid(row=2, column=0, padx=10, pady=5)
pol_var = tk.IntVar()
tk.Radiobutton(root, text="Negative (0)", variable=pol_var, value=0).grid(row=2, column=1)
tk.Radiobutton(root, text="Positive (1)", variable=pol_var, value=1).grid(row=2, column=2)

tk.Label(root, text="Power:").grid(row=3, column=0, padx=10, pady=5)
pwr_entry = tk.Entry(root)
pwr_entry.grid(row=3, column=1, columnspan=2)

tk.Label(root, text="Frequency:").grid(row=4, column=0, padx=10, pady=5)
freq_entry = tk.Entry(root)
freq_entry.grid(row=4, column=1, columnspan=2)

# Send button to initiate data send
send_button = tk.Button(root, text="Send Data", command=send_data)
send_button.grid(row=5, column=0, columnspan=3, pady=10)

# Scrolled text widget to display serial responses
tk.Label(root, text="Serial Response:").grid(row=6, column=0, columnspan=3, pady=5)
response_text = scrolledtext.ScrolledText(root, width=40, height=10)
response_text.grid(row=7, column=0, columnspan=3, padx=10, pady=5)

# Initialize serial port
serial_port = init_serial(port='COM3', baudrate=9600)

# Start a thread to read serial data continuously
serial_thread = threading.Thread(target=read_serial, daemon=True)
serial_thread.start()

# Run the main loop
root.mainloop()

# Close serial port when the GUI is closed
if serial_port:
    serial_port.close()
