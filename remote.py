#!/usr/bin/env python
# coding: utf8

import lirc
import time
import threading

class Remote:
    onKeyPress = None
    def __init__(self, onKeyPress):
        self.onKeyPress = onKeyPress
        thread = threading.Thread(target=self.__listen)
        thread.start()
    def __listen(self):
        sockid = lirc.init("sparkfun", blocking=False)

        while True:
            codeIR = lirc.nextcode()
            if codeIR != []:
                self.onKeyPress(codeIR[0])
                time.sleep(0.05)