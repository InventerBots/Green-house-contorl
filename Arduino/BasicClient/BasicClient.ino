#include <SPI.h>
#include <Ethernet.h>
#include <SparkFun_RHT03.h>

const float scale = 0.24926686217008797653958944281525; // 255/1023
const int tempData = 4;
int tempF;

byte mac[] = { 0xA6, 0x61, 0x0A, 0xAE, 0x74, 0x86 };
int port = 10003;
IPAddress ip(192,168,0,177);
IPAddress server(192,168,0,200);

RHT03 rht; // Create sensor object
EthernetClient client;

void setup() {
  Ethernet.init(10);
  Ethernet.begin(mac, ip);

  pinMode(A0, INPUT);
  Serial.begin(115200);
  while(!Serial) {
    ;
  }

  rht.begin(4);
  
  if (Ethernet.hardwareStatus() == EthernetNoHardware) {
    Serial.println("Ethernet shield not found.");
    while (true) {
     delay(25) ; // do nothing, forever...
    }
  }
  while (Ethernet.linkStatus() == LinkOFF) {
    Serial.println("No ethernet cable connected");
    delay(500);
  }
  delay(1000);
  Serial.println("Connecting");

  if (client.connect(server, port)) {
    Serial.println("connected");
  } else {
    
    Serial.println("Connection failed");
  }

  if (client.available()) {
    client.write('Hello World!');
  }
/*<------------ Debug info ------------>*/
//  Serial.print("client IP: ");
//  Serial.println(ip);
//  Serial.print("server IP: ");
//  Serial.println(server);
//  Serial.print("local IP: ");
//  Serial.println(Ethernet.localIP());
//  Serial.print("remote IP: ");
//  Serial.println(client.remoteIP());
//  Serial.print("remote port: ");
//  Serial.println(client.remotePort());
//  Serial.print("local port: ");
//  Serial.println(client.localPort());
//  Serial.print("connect feed back: ");
//  Serial.println(client.connect(server, port));
}

void loop() {
  int tempRaw = analogRead(A0);
  if (client.available()) {
    char c = client.read();
    
    
    Serial.print(c);
  }
  //Serial.println(tempRaw); 
  client.print(tempRaw);
  
  while (Serial.available()) {
    char inChar = Serial.read();
    if (Serial.read() == "e") {
      Serial.println("exiting");
      //stopClient(client);
    }
    
    if (client.connected()) {
      client.write(inChar);
    }
  }

 if (!client.connected()) {
    stopClient(client);
  }

  delay(500);
}

void stopClient(EthernetClient eClient) {
  Serial.println();
  Serial.println("Disconnecting");
  eClient.stop();
  while (true) {
    delay(25);
  }
}
