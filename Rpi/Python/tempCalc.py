import server

from collections import deque
import numpy
import time

avrageRise:float = 0
logSet = deque([])
tempVal = []
curVal = []
rise = []
bufferLength = 2

inputQue = deque([])

def formatTemp(unit, rawTemp=[]):
    temp = []
    for x in range(len(rawTemp)):
        match unit:
            case "F": 
                temp.append(server.Server.convertRawToDeg_F(rawTemp[x]))
            case "C":
                temp.append(server.Server.convertRawToDeg_C(rawTemp[x]))
            case "K":
                temp.append(server.Server.convertRawToDeg_K(rawTemp[x]))
            case _:
                raise Exception('Invalid temperature unit')
    rawTemp.clear()
    return temp

def tempRise(bufferLen, que=deque([])):
    bufferLength = bufferLen
    curVal:int = 5
    curentTemp = []
    pastTemp = []
    
    # for _set1 in range(len(que[0])):
    #     rise = 0
    # try:
    curentTemp = numpy.array(que[0])
    pastTemp = numpy.array(que[1])
    # print(curentTemp, pastTemp)
    # print(que)
    rise = numpy.subtract(curentTemp, pastTemp)
    # print(rise)

    # print(rise)
    # que.clear()
    
    # print(curentTemp, pastTemp)
    # for z in range(len(curentTemp)):
    #     rise.append(numpy.subtract(pastTemp, curentTemp))
    # print(rise)

    logSet.append(rise)
    if len(logSet) > bufferLength:
        logSet.popleft()
    # print(len(logSet), '\t', logSet)

    # avrageRise = sum(list(logSet[0])) / len(list(logSet[0]))

    if __name__ == '__main__':
        # print('rise:       ', rise)
        # print('temp:       ', curVal)
        # print('total rise: ', avrageRise)
        # print(len(logSet))
        print()
        # print(tempVal, server.Server.convertRawToDeg_F(server.tempRaw_12bit_int[0]))
        # print(rawVal)
    return rise
    # except:
    #     raise Exception('Formated temperature not found')


if __name__ == "__main__":
    bufferLength = 10

    server.Server.connect(server)
    for _ in range(12):
        server.Server.read_rawTemp(server, 3)
        inputQue.append(server.tempRaw_12bit_int)
        if len(inputQue) > 2:
            inputQue.popleft()
            tempRise(4, inputQue)
        print(inputQue)            
        
        time.sleep(1)
    server.Server.disconnect(server)
