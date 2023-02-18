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
        if unit == "F": 
            temp.append(server.Server.convertRawToDeg_F(rawTemp[x]))
        elif unit == "C":
            temp.append(server.Server.convertRawToDeg_C(rawTemp[x]))
        elif unit == "K":
            temp.append(server.Server.convertRawToDeg_K(rawTemp[x]))
        else:
            raise Exception('Invalid temperature unit')
    rawTemp.clear()
    return temp

def tempRise(predictTime, tempUnit, bufferLen, que=deque([])):
    bufferLength = bufferLen
    curentTemp = []
    pastTemp = []
    
    # for _set1 in range(len(que[0])):
    #     rise = 0
 
    curentTemp = que[0]
    pastTemp = que[1]

    for c in range(len(curentTemp)):
        curentTemp_deg = numpy.array(server.Server.convertRawToDeg_F(curentTemp[c]))
    for p in range(len(pastTemp)):
        pastTemp_deg = numpy.array(server.Server.convertRawToDeg_F(pastTemp[p]))
    rise = numpy.subtract(pastTemp_deg, curentTemp_deg)
    curentTemp_avg = numpy.average(curentTemp_deg)
    # print(rise)

    logSet.append(rise)
    if len(logSet) > bufferLength:
        logSet.popleft()
    # print(len(logSet), '\t', logSet)
    print('Dataset size:', len(logSet))
    avrageRise = numpy.average(logSet)
    # print(avrageRise, curentTemp_avg)
    
    print('%.2f' % ((avrageRise*predictTime)+curentTemp_avg))

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
