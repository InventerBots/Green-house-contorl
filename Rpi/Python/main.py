import codecs
import socket
from turtle import delay

HOST = '0.0.0.0' # server IP
PORT = 10004

RELAY_ON = bytes(1)
RELAY_OFF = bytes(0)

startup = 0

INPUT_NUM = 4

tempRaw = 0 #[0, 0, 0, 0, 0] # temp0, temp1, temp2, temp3, extTemp

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
  s.bind((HOST, PORT))
  s.listen()
  conn, addr = s.accept()
  with conn:
    print('Connected by', addr)
    
    while (startup == 0) : # only run once when app is first loaded
      # INPUT_NUM = int(conn.recv(1023)) + 1 # record number of snesors connected to client
      # print ("Number of sensors connected: ", INPUT_NUM)
      startup = 1 

    while (True) : # main loop
      sensorIndex = 0
      data_12bit_int = 0
      data_12bit_Raw = conn.recv(4096)
      dataIsStr = False

      # try to convert incoming data to intiger form, if unable, convert to string
      try:
        data_12bit_int = int(data_12bit_Raw)
      except:
        decData = codecs.decode(data_12bit_Raw)
        continue
      # print("data is strig:" , decData)
      
      if (decData == 'INDEX') :
        indexMode = 0
        while(indexMode == 0) :
          if (data_12bit_int > 0 and data_12bit_int <= INPUT_NUM) :
            sensorIndex = data_12bit_int
            indexMode = 1
          else :
            tempRaw = data_12bit_int
            indexMode = 1

# todo return 1 if index and sensor data receved, -1 if not
          
      print(data_12bit_int)
      # print('index, value: ', sensorIndex, '\t', data_12bit_int)

      

    # while True:
    #   #--- temperature calculations ---#
    #   # tempK=1/((1/298.15)+(1/3977)*math.log((10000/(1023/int(conn.recv(1023))-1))/10000))
    #   # tempF=(tempK-273.15)*(9/5)+32
    #   # print("Receved: ", tempF)
    #   data=int(conn.recv(1023))
    #   sensorNum=0
      
    #   msg='init'
    #   if str(data)==msg:
    #       sensorNum=data
    #       print(sensorNum)

    #   if data < 1024:
    #     for i in range (0, 3):
    #       tempRaw[i]=data
    #   print(tempRaw)

    #   # tempRawAvrage=mean(tempRaw)
    #   # if tempRawAvrage>10:
    #   #   tempK=1/((1/298.15)+(1/3977)*math.log((10000/(1023/int(tempRawAvrage)-1))/10000))

    #   tempF=(tempK-273.15)*(9/5)+32