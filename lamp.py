import RPi.GPIO as GPIO
import setinterval


class Lamp:
    freq = 200

    currentred = 0
    currentgreen = 100
    currentblue = 100

    webRed = 255
    webGreen = 0
    webBlue = 0

    ISRUNNING = False

    timerRed = 0
    timerGreen= 0
    timerBlue = 0
    timerDirection = "down"
    timerOn = True
    timer = None
    timerName = "off"
    timerPeriod = 1

    def __init__(self, pinRed, pinGreen, pinBlue, isOn = True, red = 0, green = 0, blue = 0):
        self.pinRed = pinRed
        self.pinGreen = pinGreen
        self.pinBlue = pinBlue
        self.start()
        self.color(red, green, blue)

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
            if self.timer is not None:
                self.timer.cancel()
            self.timerOn = True
            self.timer = setinterval.SetInterval(self.timerPeriod, self.blink)
            self.timerName = "blinking"
            print("Start blinking")
        elif t == "pulsating":
            if self.timer is not None:
                self.timer.cancel()
            self.timerDirection = "down"
            self.timerRed = self.webRed
            self.timerGreen = self.webGreen
            self.timerBlue = self.webBlue
            self.timer = setinterval.SetInterval(self.getInterval(), self.pulsate)
            self.timerName = "pulsating"
            print("Start pulsating")
        else:
            if self.timer is not None:
                self.timer.cancel()
                self.timer = None
            self.timerName = "off"
            self.__colorInternal(self.webRed, self.webGreen, self.webBlue)

    def getInterval(self):
        maxAmount = max(self.webRed, self.webGreen, self.webBlue)
        return float(self.timerPeriod) / float(maxAmount)

    def period(self, newperiod):
        self.timerPeriod = newperiod

    def blink(self):
        self.timer.setInterval(self.timerPeriod)
        if self.timerOn:
            self.__colorInternal(0, 0, 0)
        else:
            self.__colorInternal(self.webRed, self.webGreen, self.webBlue)
        self.timerOn = not self.timerOn

    def pulsate(self):
        self.timer.setInterval(self.getInterval())
        if self.timerDirection == "up":
            if self.timerRed < self.webRed or self.timerGreen < self.webGreen or self.timerBlue < self.webBlue:
                if self.timerRed < self.webRed:
                    self.timerRed = self.timerRed + 1
                if self.timerGreen < self.webGreen:
                    self.timerGreen = self.timerGreen + 1
                if self.timerBlue < self.webBlue:
                    self.timerBlue = self.timerBlue + 1
            else:
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
                self.timerDirection = "up"
        self.__colorInternal(self.timerRed, self.timerGreen, self.timerBlue)
