#!/usr/bin/env python
# coding: utf8

import lirc
import time
import threading

class Remote:
    onKeyPress = None
    isRunning = True
    def __init__(self, onKeyPress):
        self.onKeyPress = onKeyPress
        self.thread = threading.Thread(target=self.__listen)
        self.thread.start()
    def __listen(self):
        sockid = lirc.init("sparkfun", blocking=False)

        while self.isRunning:
            codeIR = lirc.nextcode()
            if codeIR != []:
                self.onKeyPress(codeIR[0])
            time.sleep(0.1)

    def destroy(self):
        self.isRunning = False
