import RPi.GPIO as GPIO


class Lamp:
    red = 16
    green = 20
    blue = 21
    freq = 100

    currentred = 0
    currentblue = 0
    currentgreen = 0

    def start(self):
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

        self.RED.ChangeDutyCycle(self.currentred)
        self.GREEN.ChangeDutyCycle(self.currentgreen)
        self.BLUE.ChangeDutyCycle(self.currentblue)

        self.ISRUNNING = True

    def stop(self):
        self.ISRUNNING = False
        GPIO.cleanup()

    def destroy(self):
        GPIO.cleanup()

    def color(self, red, green, blue):
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