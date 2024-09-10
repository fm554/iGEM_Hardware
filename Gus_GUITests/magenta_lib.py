import RPi.GPIO as GPIO
import serial

def img_mode(mode, white = 23, blue = 24):
    if mode == 0 | mode == "off":
        GPIO.output(white, False)
        GPIO.output(blue, False)
    elif mode == 1 | mode == "Std":
        GPIO.output(white, True)
        GPIO.output(blue, False)
    elif mode == 2 | mode == "Fluoro":
        GPIO.output(white, False)
        GPIO.output(blue, True)
    else:
        raise Exception("Invalid Image Mode")

def coil_power():
    pass

def move_motor():
    pass

def calibrate_motor():
    pass
def write_display():
    pass


