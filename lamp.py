import RPi.GPIO as GPIO


class Lamp:
    def __init__(self, red: int = 16, green: int = 20, blue: int = 21, freq: int = 100):
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

    def color(self, red: int, green: int, blue: int):
        self.RED.ChangeDutyCycle(100 - red / 255)
        self.GREEN.ChangeDutyCycle(100 - green / 255)
        self.RED.ChangeDutyCycle(100 - blue / 255)
