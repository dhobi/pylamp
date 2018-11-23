import RPi.GPIO as GPIO


class Lamp:
    red = 16
    green = 20
    blue = 21
    freq = 100

    currentred = 100
    currentblue = 100
    currentgreen = 100

    def __init__(self):
        print('lamp initialising...')
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)

        GPIO.setup(self.red, GPIO.OUT)
        GPIO.setup(self.green, GPIO.OUT)
        GPIO.setup(self.blue, GPIO.OUT)

        self.RED = GPIO.PWM(self.red, self.freq)
        self.GREEN = GPIO.PWM(self.green, self.freq)
        self.BLUE = GPIO.PWM(self.blue, self.freq)

        self.RED.start(self.currentred)
        self.GREEN.start(self.currentgreen)
        self.BLUE.start(self.currentblue)

        self.start()
        print('...done.')

    def start(self):
        self.ISRUNNING = True
        self.RED.ChangeDutyCycle(self.currentred)
        self.GREEN.ChangeDutyCycle(self.currentgreen)
        self.BLUE.ChangeDutyCycle(self.currentblue)

    def stop(self):
        self.RED.ChangeDutyCycle(100)
        self.GREEN.ChangeDutyCycle(100)
        self.BLUE.ChangeDutyCycle(100)
        self.ISRUNNING = False

    def destroy(self):
        print('resetting lamp')
        GPIO.cleanup()

    def color(self, red, green, blue):
        print('Set lamp to r' + str(red) + ', g' + str(green) + ', b' + str(blue))
        self.currentred = 100 - red / 2.55
        self.currentgreen = 100 - green / 2.55
        self.currentblue = 100 - blue / 2.55

        if self.ISRUNNING:
            self.RED.ChangeDutyCycle(self.currentred)
            self.GREEN.ChangeDutyCycle(self.currentgreen)
            self.BLUE.ChangeDutyCycle(self.currentblue)

    def toggle(self):
        if self.ISRUNNING:
            self.stop()
        else:
            self.start()