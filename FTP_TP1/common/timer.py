import time


class timer:

    def __init__():
        self.timeoutInterval = 1000
        self.ALPHA = 0.125
        self.BETA = 0.25
        self.estimatedRTT = 0
        self.devRTT = 0
        self.sendTime = -1

    def calculateTimeout():
        ackTime = time.now()
        sampleRTT = ackTime - self.sendTime

        self.estimatedRTT = self.estimatedRTT * (1 - ALPHA) * self.estimatedRTT + ALPHA * sampleRTT
        self.devRTT = (1 - BETA) * self.devRTT + BETA * abs(sampleRTT - self.estimatedRTT)

        self.timeoutInterval = estimatedRTT + 4 * devRTT

    def getTimeout():
        return self.timeoutInterval

    def sentPacket():
        self.sendTime = time.now()

    def timeout():
        self.timeoutInterval *= 2

