# defining the RPi's pins as Input / Output
import RPi.GPIO as GPIO

# importing the library for delaying command.
import time

# used for GPIO numbering
GPIO.setmode(GPIO.BCM)

# closing the warnings when you are compiling the code
GPIO.setwarnings(False)

RUNNING = True

# defining the pins
red = 16
green = 20
blue = 21

# defining the pins as output
GPIO.setup(red, GPIO.OUT)
GPIO.setup(green, GPIO.OUT)
GPIO.setup(blue, GPIO.OUT)

# choosing a frequency for pwm
Freq = 100

# defining the pins that are going to be used with PWM
RED = GPIO.PWM(red, Freq)
GREEN = GPIO.PWM(green, Freq)
BLUE = GPIO.PWM(blue, Freq)

try:
    # we are starting with the loop
    while RUNNING:
        # lighting up the pins. 100 means giving 100% to the pin
        RED.start(100)
        GREEN.start(100)
        BLUE.start(100)

        print('Red')
        for x in range(1, 101):
            RED.ChangeDutyCycle(101 - x)
            time.sleep(0.025)

        RED.ChangeDutyCycle(100)
        print('Green')
        for x in range(1, 101):
            GREEN.ChangeDutyCycle(101 - x)
            time.sleep(0.025)

        GREEN.ChangeDutyCycle(100)
        print('Blue')
        for x in range(1, 101):
            BLUE.ChangeDutyCycle(101 - x)
            time.sleep(0.025)

        BLUE.ChangeDutyCycle(100)

except KeyboardInterrupt:
    RUNNING = False
    GPIO.cleanup()