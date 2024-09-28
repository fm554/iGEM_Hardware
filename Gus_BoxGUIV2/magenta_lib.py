import gpiod
import time
import serial
import atexit
def img_mode(serial, mode, white_line, blue_line):
    if mode == 0:
        serial.write(b"Img: off\n")
        white_line.set_value(0)
        blue_line.set_value(0)
    elif mode == 1:
        serial.write(b"Img: std\n")
        white_line.set_value(1)
        blue_line.set_value(0)
    elif mode == 2:
        serial.write(b"Img: fluoro\n")
        white_line.set_value(0)
        blue_line.set_value(1)
    else:
        raise Exception("Invalid Image Mode")

def coil_power():
    #TODO
    pass

def move_motor(serial, motor, position):
    msg = motor + " Motor: " + str(position) + "\n"
    serial.write(msg.encode('utf-8'))

def calibrate_motor(serial, motor):
    msg = "Calibrate: " + motor + "\n"
    serial.write(msg.encode('utf-8'))
def write_display(serial, string):
    #max 16 characters
    serial.write(string)

# print(type(b"test"))
# white_GPIO = 23
# blue_GPIO = 24
# serial_port=serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
# chip = gpiod.Chip('gpiochip0')
# white_line = chip.get_line(white_GPIO)
# white_line.request(consumer="LED", type=gpiod.LINE_REQ_DIR_OUT)
# blue_line = chip.get_line(blue_GPIO)
# blue_line.request(consumer="LED", type=gpiod.LINE_REQ_DIR_OUT)

# serial_port=serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
# time.sleep(5)
# calibrate_motor(serial_port, "X")
# move_motor(serial_port, "X", 20.5)
#move_motor(serial_port, "X", 20)


# try:
#     for i in range(10):
#         img_mode(serial_port, 0, white_line, blue_line)
#         time.sleep(1)
#         img_mode(serial_port, 1, white_line, blue_line)
#         time.sleep(1)
#         img_mode(serial_port, 2, white_line, blue_line)
#         time.sleep(1)
# finally:
#     white_line.set_value(0)
#     blue_line.set_value(0)
#     white_line.release()
#     blue_line.release()
# img_mode(serial_port, 0)
# print("sent")


