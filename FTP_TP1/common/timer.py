import time


class Timer:

    def __init__(self):
        self.timeoutInterval = 1
        self.ALPHA = 0.125
        self.BETA = 0.25
        self.estimatedRTT = 0
        self.devRTT = 0
        self.sendTime = -1

    def calculateTimeout(self, sample):
        self.estimatedRTT = self.estimatedRTT * \
            (1 - self.ALPHA) * self.estimatedRTT + self.ALPHA * sample
        self.devRTT = (1 - self.BETA) * self.devRTT + \
            self.BETA * abs(sample - self.estimatedRTT)

        self.timeoutInterval = self.estimatedRTT + 4 * self.devRTT

    def getTimeout(self):
        return min(self.timeoutInterval, 1)

    def timeout(self):
        self.timeoutInterval *= 2
