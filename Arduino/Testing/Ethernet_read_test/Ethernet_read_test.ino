#include <SPI.h>
#include <Ethernet.h>

uint8_t mac[] = { 0xA6, 0x61, 0x0A, 0xAE, 0x74, 0x86};
int port = 10004;

IPAddress ip(192, 168, 1, 178);
IPAddress server(192, 168, 1, 220);

EthernetClient client;

void setup() {
  Serial.begin(115200);
  while(!Serial) { // wait for serial port to open
    ;
  }
  Serial.println("serial is running");

   Ethernet.init(10); // use pin 10 for chip slect
   Ethernet.begin(mac, ip); // start ethernet socket

   bool hardwareStatus = false;
   while (!hardwareStatus) {
     if (Ethernet.hardwareStatus() == EthernetNoHardware) {
       Serial.println("No Ethernet hardware found");
       delay(2500);
     } else {
       Serial.println("Ethernet hardware found");
       hardwareStatus == true;
       break;
     }
   }

   while (Ethernet.linkStatus() == LinkOFF) {
   Serial.println("No ethernet cable connected");
   delay(2500);
   }

   Serial.println("Connecting");

   while (!client.connected()) {
     if (client.connect(server, port)) {
       Serial.print("Connected to ");
       Serial.println(server);
      //  client.print(NUM_SENSOR_CONNECTED); // tell the server how many sensors to read
       client.flush();
       break;
     } else {
       Serial.println("Connection fialed");
       delay(3000); // wait 3 secconds before trying to connect again
     }
   }
}

void loop() {
  if (client.available()) {
    char c = client.read();
    Serial.println(int(client.read()));
  }
  while (!client.available()) {
    ;
  }
  
  client.flush();
  
  if (!client.connected()) {
    client.stop();
    Serial.println("Server disconnected, restarting");
    delay(5000);
    setup();
  }
}
