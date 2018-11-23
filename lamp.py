import RPi.GPIO as GPIO


class Lamp:
    red = 16
    green = 20
    blue = 21
    freq = 100

    def __init__(self):
        print('lamp initialising...')
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)

        GPIO.setup(self.red, GPIO.OUT)
        GPIO.setup(self.green, GPIO.OUT)
        GPIO.setup(self.blue, GPIO.OUT)

        GPIO.output(self.red, 1)
        GPIO.output(self.green, 1)
        GPIO.output(self.blue, 1)

        self.RED = GPIO.PWM(self.red, self.freq)
        self.GREEN = GPIO.PWM(self.green, self.freq)
        self.BLUE = GPIO.PWM(self.blue, self.freq)

        self.start()
        print('...done.')

    def start(self):
        self.RED.start(100)
        self.GREEN.start(100)
        self.BLUE.start(100)
        self.ISRUNNING = True

    def stop(self):
        self.RED.stop()
        self.GREEN.stop()
        self.BLUE.stop()

        GPIO.output(self.red, 1)
        GPIO.output(self.green, 1)
        GPIO.output(self.blue, 1)

        self.ISRUNNING = False

    def destroy(self):
        print('resetting lamp')
        GPIO.cleanup()

    def color(self, red, green, blue):
        print('Set lamp to r' + str(red) + ', g' + str(green) + ', b' + str(blue))
        self.RED.ChangeDutyCycle(100 - red / 2.55)
        self.GREEN.ChangeDutyCycle(100 - green / 2.55)
        self.BLUE.ChangeDutyCycle(100 - blue / 2.55)

    def toggle(self):
        if self.ISRUNNING:
            self.stop()
        else:
            self.start()