from collections import deque
import numpy

avrageRise:float = 0
logSet = deque([])
tempVal = []
curVal = []
rise = []
bufferLength = 2

inputQue = deque([])

def convertRawToDeg_K (rawTemp):
        try:
            R = 10000 / (4096 / int(rawTemp) - 1)
            return 1/((1/298.15)+(1/3977)*numpy.log(R/10000))
        except:
            Exception()
    
def convertRawToDeg_F (rawTemp):
    try:
        R = 10000 / (4096 / int(rawTemp) - 1)
        tempK = 1/((1/298.15)+(1/3977)*numpy.log(R/10000)) 
        return (tempK) * (9/5) - 459.67
    except:
        Exception()

def convertRawToDeg_C (rawTemp):
    try:
        R = 10000 / (4096 / int(rawTemp) - 1)
        tempK = 1/((1/298.15)+(1/3977)*numpy.log(R/10000))
        return (tempK) - 273.15
    except:
        Exception()

def formatTemp(unit, rawTemp=[]):
    temp = []
    for x in range(len(rawTemp)):
        if unit == "F": 
            temp.append(convertRawToDeg_F(rawTemp[x]))
        elif unit == "C":
            temp.append(convertRawToDeg_C(rawTemp[x]))
        elif unit == "K":
            temp.append(convertRawToDeg_K(rawTemp[x]))
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
        curentTemp_deg = numpy.array(convertRawToDeg_F(curentTemp[c]))
    for p in range(len(pastTemp)):
        pastTemp_deg = numpy.array(convertRawToDeg_F(pastTemp[p]))
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