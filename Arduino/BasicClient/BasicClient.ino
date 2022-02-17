#include <SPI.h>
#include <Ethernet.h>

byte mac[] = { 0xA6, 0x61, 0x0A, 0xAE, 0x74, 0x86 };
int port = 8;
IPAddress ip(169,254,25,177);
IPAddress server(169,254,80,147);

EthernetClient client;

void setup() {
  Ethernet.init(10);
  Ethernet.begin(mac, ip);

//  Ethernet.setLocalIP(ip);
//  Ethernet.setMACAddress(mac);
//  Ethernet.setDnsServerIP(server);
//  Ethernet.remotePort(port);
  
  
  Serial.begin(115200);
  while(!Serial) {
    ;
  }
  
  if (Ethernet.hardwareStatus() == EthernetNoHardware) {
    Serial.println("Ethernet shield not found.");
    while (true) {
      ; // do nothing, forever...
    }
  }
  while (Ethernet.linkStatus() == LinkOFF) {
    Serial.println("No ethernet cable connected");
    delay(500);
  }
  delay(1000);
  Serial.println("Connecting");

  if (client.connect(server, 8)) {
    Serial.println("connected");
  } else {
    
    Serial.println("Connection failed");
  }

  
  Serial.print("remote IP: ");
  Serial.println(client.remoteIP());
  Serial.print("remote port: ");
  Serial.println(client.localPort());
  Serial.print("local port: ");
  Serial.println(client.localPort());
  Serial.print("connect feed back: ");
  Serial.println(client.connect(server, 8));
}

void loop() {
  if (client.available()) {
    client.print("Hello World");
    char c = client.read();
    Serial.print(c);
  }

 if (!client.connected()) {
  Serial.println();
  Serial.println("Disconnecting");
  client.stop();
  while (true) {
    delay(1);
  }
 }
}
