from pigpio import pi
import setinterval

class LampHw(pi):
    def __init__(self, red_pin, green_pin, blue_pin, on=True, red_value=0, green_value=0, blue_value=0):
        pi.__init__(self)
        self.__r_pin = red_pin
        self.__g_pin = green_pin
        self.__b_pin = blue_pin
        # store on state
        self.ISRUNNING = on
        # store RGB values
        self.webRed = red_value
        self.webGreen = green_value
        self.webBlue = blue_value

        self.timer = None
        self.timerOn = False
        self.timerName = "off"
        self.timerPeriod = 1
        self.timerDirection = "up"
        self.timerRed = 0
        self.timerGreen = 0
        self.timerBlue = 0

        # refresh to set default RGB values
        self.__refresh()

    def __refresh(self):
        self.set_PWM_dutycycle(self.__r_pin, 255 - self.webRed if self.ISRUNNING else 0)
        self.set_PWM_dutycycle(self.__g_pin, 255 - self.webGreen if self.ISRUNNING else 0)
        self.set_PWM_dutycycle(self.__b_pin, 255 - self.webBlue if self.ISRUNNING else 0)

    def color(self, red_value, green_value, blue_value):
        self.webRed = red_value
        self.webGreen = green_value
        self.webBlue = blue_value
        self.__refresh()

    def toggle(self):
        if self.ISRUNNING:
            self.turn_off()
        else:
            self.turn_on()

    def turn_on(self):
        self.ISRUNNING = True
        self.__refresh()

    def turn_off(self):
        self.ISRUNNING = False
        self.__refresh()

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
            self.color(self.webRed, self.webGreen, self.webBlue)

    def getInterval(self):
        maxAmount = max(self.webRed, self.webGreen, self.webBlue)
        if maxAmount == 0:
            maxAmount = 1
        return float(self.timerPeriod) / float(maxAmount)

    def period(self, newperiod):
        self.timerPeriod = newperiod

    def blink(self):
        self.timer.setInterval(self.timerPeriod)
        if self.timerOn:
            self.color(0, 0, 0)
        else:
            self.color(self.webRed, self.webGreen, self.webBlue)
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
        self.color(self.timerRed, self.timerGreen, self.timerBlue)

    def destroy(self):
        self.turn_off()