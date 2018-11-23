import RPi.GPIO as GPIO


class Lamp:
    def __init__(self, red = 16, green = 20, blue = 21, freq = 100):
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)

        GPIO.setup(red, GPIO.OUT)
        GPIO.setup(green, GPIO.OUT)
        GPIO.setup(blue, GPIO.OUT)

        self.RED = GPIO.PWM(red, freq)
        self.GREEN = GPIO.PWM(green, freq)
        self.BLUE = GPIO.PWM(blue, freq)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        GPIO.cleanup()

    def color(self, red, green, blue):
        print('Set lamp to r'+str(red)+', g'+str(green)+', b'+str(blue))
        self.RED.ChangeDutyCycle(100 - red / 2.55)
        self.GREEN.ChangeDutyCycle(100 - green / 2.55)
        self.RED.ChangeDutyCycle(100 - blue / 2.55)
