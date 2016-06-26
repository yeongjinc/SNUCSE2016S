import math
import random

# Unit : micro sec
# No error assumption
PACKET_SIZE = 1024 * 8
TRANSMISSION_RATE = 10.0 * 1024 * 1024 / 1000 / 1000
TRANSMISSION_TIME = int(PACKET_SIZE / TRANSMISSION_RATE)
SLOT_TIME = 50
COLLISION_CRITERIA = 50
MEAN_INTERVAL = 10 * 1000
MAX_TIME = 1000000
ITERATION_COUNT = 1

ACK_TRANSMISSION_TIME = 40 # assumption

M = ["CSMA", "CSMA/CD", "CSMA/CD/BEB"]
N = [5, 10, 15, 20, 25]
CW = [32, 64, 128]

'''
M = ["CSMA", "CSMA/CD", "CSMA/CD/BEB"]
N = [15]
CW = [32]
'''

class Station:
    send = False
    sendTime = 0
    transTime = 0
    backoffTime = 0
    backoff = 0
    transCount = 0
    collisionCount = 0
    countDelay = False
    delay = 0

def Simulate():
    for mode in M:
        for n in N:
            for cw in CW:
                if mode == 'CSMA/CD/BEB' and cw <= 32: # for execute once
                    print ('Mode=' + mode + ', N=' + str(n) + ', CW is binary exponential')
                elif mode == 'CSMA/CD/BEB' and cw > 32:
                    break
                else:
                    print ('Mode=' + mode + ', N=' + str(n) + ', CW=' + str(cw))

                # for iter
                gSumPacket = 0
                gSumCollision = 0
                gSumDelay = 0

                for iterCnt in range(0, ITERATION_COUNT):
                    clock = 0
                    stations = []

                    sendStation = None
                    isSending = False

                    for i in range(0, n):
                        stations.append(Station())

                    # clock iteration
                    for c in range(0, MAX_TIME):
                        # set next transmission when ends
                        for s in stations:
                            if s.send == False:
                                # add epsilon for prevent ln(0)
                                # add 1 for decrease here
                                s.sendTime = (int)(-math.log(random.random() + 0.00000000001) * MEAN_INTERVAL) + 1
                                s.send = True
                                s.countDelay = False
                                s.backoff = 0
                                s.transCount += 1

                        # decrease timer clock
                        for s in stations:
                            if s.sendTime > 0:
                                s.sendTime -= 1
                            if s.transTime > 0:
                                s.transTime -= 1
                            if s.countDelay == True:
                                s.delay += 1
                            if isSending == False and s.backoffTime > 0:
                                s.backoffTime -= 1

                        # send if send timer is 0
                        # handle collision
                        collision = False
                        for s in stations:
                            if s == sendStation:
                                break
                            if s.sendTime == 0 and s.backoffTime == 0:
                                s.countDelay = True
                                if isSending == False:
                                    isSending = True
                                    s.transTime = TRANSMISSION_TIME
                                    if mode == 'CSMA':
                                        s.transTime += ACK_TRANSMISSION_TIME
                                    sendStation = s
                                elif mode == 'CSMA' and TRANSMISSION_TIME - sendStation.transTime < COLLISION_CRITERIA + ACK_TRANSMISSION_TIME:
                                    collision = True
                                    sCW = sendCW = cw
                                    s.backoffTime = random.randrange(1, sCW) * SLOT_TIME
                                    s.collisionCount += 1
                                elif TRANSMISSION_TIME - sendStation.transTime < COLLISION_CRITERIA:
                                    # collision occurs
                                    # both stations cancel and backoff
                                    collision = True
                                    if mode == 'CSMA/CD/BEB':
                                        s.backoff += 1
                                        if s.backoff > 10:
                                            s.backoff = 10
                                        sCW = 2 ** s.backoff

                                        sendStation.backoff += 1
                                        if sendStation.backoff > 10:
                                            sendStation.backoff = 10
                                        sendCW = 2 ** sendStation.backoff
                                    else:
                                        sCW = sendCW = cw

                                    s.backoffTime = random.randrange(1, sCW) * SLOT_TIME
                                    s.collisionCount += 1

                                    sendStation.backoffTime = random.randrange(1, sendCW) * SLOT_TIME
                                    sendStation.collisionCount += 1

                                    isSending = False
                                    sendStation = None
                                #else:
                                    # carrier sense and wait
                                    # do nothing

                        if mode == 'CSMA' and collision == True:
                            sendStation.sendTime = random.randrange(1, sendCW) * SLOT_TIME
                            sendStation.collisionCount += 1
                            isSending = False
                            sendStation = None

                        if sendStation is not None:
                            if sendStation.transTime == 0:
                                sendStation.send = False
                                isSending = False
                                sendStation = None

                    sumPacket = 0
                    sumCollision = 0
                    sumDelay = 0
                    for s in stations:
                        sumPacket += s.transCount
                        sumCollision += s.collisionCount
                        sumDelay += s.delay

                    sec = MAX_TIME / 1000000
                    print ('Throughput=' + str(sumPacket * 1.0 / sec))
                    print ('Mean Packet Delay=' + str(sumDelay * 1.0 / sumPacket))
                    print ('Collision Probability=' + str(sumCollision * 1.0 / (sumPacket+sumCollision)))


                    gSumPacket += sumPacket
                    gSumCollision += sumCollision
                    gSumDelay += sumDelay

                    if ITERATION_COUNT > 1:
                        print ('Total statistics : sec or propotional')
                        print ('Total Throughput=' + str(gSumPacket * 1.0 / sec))
                        print ('Total Mean Packet Delay=' + str(gSumDelay * 1.0 / gSumPacket))
                        print ('Total Collision Probability=' + str(gSumCollision * 1.0 / (gSumPacket + gSumCollision)))

Simulate()
