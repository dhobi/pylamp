import RPi.GPIO as GPIO
import setinterval


class Lamp:
    pinRed = 16
    pinGreen = 20
    pinBlue = 21
    freq = 100

    currentred = 100
    currentgreen = 100
    currentblue = 100

    webRed = 0
    webGreen = 0
    webBlue = 0

    ISRUNNING = False

    timerRed = 0
    timerGreen= 0
    timerBlue = 0
    timerDirection = "down"
    timer = None

    def start(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)

        GPIO.setup(self.pinRed, GPIO.OUT)
        GPIO.setup(self.pinGreen, GPIO.OUT)
        GPIO.setup(self.pinBlue, GPIO.OUT)

        self.RED = GPIO.PWM(self.pinRed, self.freq)
        self.GREEN = GPIO.PWM(self.pinGreen, self.freq)
        self.BLUE = GPIO.PWM(self.pinBlue, self.freq)

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
        if self.timer is not None:
            self.timer.cancel()

    def color(self, red, green, blue):
        self.webRed = red
        self.webGreen = green
        self.webBlue = blue
        self.__colorInternal(red, green, blue)

    def __colorInternal(self, red, green, blue):
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

    def type(self, t):
        if t == "blinking":
            if self.timer is None:
                print("starting blink")
                self.timerDirection = "down"
                self.timerRed = self.webRed
                self.timerGreen = self.webGreen
                self.timerBlue = self.webBlue
                self.timer = setinterval.SetInterval(0.002, self.blink)
        else:
            if self.timer is not None:
                self.timer.cancel()
                self.timer = None

    def blink(self):
        if self.timerDirection == "up":
            if self.timerRed < self.webRed or self.timerGreen < self.webGreen or self.timerBlue < self.webBlue:
                if self.timerRed < self.webRed:
                    self.timerRed = self.timerRed + 1
                if self.timerGreen < self.webGreen:
                    self.timerGreen = self.timerGreen + 1
                if self.timerBlue < self.webBlue:
                    self.timerBlue = self.timerBlue + 1
            else:
                print('change blink direction to down')
                self.timerDirection = "down"
        else:
            if self.timerRed > 0 or self.timerGreen > 0 or self.timerBlue > 0:
                if self.timerRed > 0:
                    self.timerRed = self.timerRed - 1
                if self.timerGreen > 0:
                    self.timerGreen = self.timerGreen - 1
                if self.timerBlue > 0:
                    self.timerBlue = self.timerBlue - 1
            else:
                print('change blink direction to up')
                self.timerDirection = "up"
        self.__colorInternal(self.timerRed, self.timerGreen, self.timerBlue)
