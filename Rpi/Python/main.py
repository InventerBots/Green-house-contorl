import server
from time import sleep

server.connect()
print (server.Connected_IP)

for x in range(4):
  server.read_rawTemp(4)
  print(server.tempRaw_12bit_int)
  sleep(2)

server.disconnect()