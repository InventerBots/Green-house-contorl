#include <SPI.h>
#include <Ethernet.h>

int tempF;

byte mac[] = { 0xA6, 0x61, 0x0A, 0xAE, 0x74, 0x86 };
int port = 10004;
IPAddress ip(192, 168, 1, 177);
IPAddress server(192, 168, 1, 220);

EthernetClient client;

void setup() {
  Ethernet.init(10);
  Ethernet.begin(mac, ip);

  pinMode(A0, INPUT);
  pinMode(A1, INPUT);
  pinMode(A2, INPUT);
  pinMode(2, OUTPUT);
  
  Serial.begin(115200);
  while (!Serial) {
    ;
  }


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
  // store all three sesnors in one array
  int sensorVal[3] = {analogRead(A0), analogRead(A1), analogRead(A2)};
  
  float tempRaw = analogRead(A0);
  float iRawTemp = abs((((tempRaw * 10) / (1023 * 10)) - 1) * 1023);
  int intTempRaw = (int)iRawTemp;

  //Serial.print("inverted:");
  //Serial.println(iRawTemp);
  //client.print((int)tempRaw);
  //Serial.println(tempRaw);

  for(int x=0;x<3;x++) {
    Serial.print("x: ");
    Serial.println(x);
    Serial.println(sensorVal[x]);
    client.print(x);
    client.print(sensorVal[x]);
  }

  //Serial.print("relay: ");
  int relay = client.read()+1;
  //Serial.println(relay);
  digitalWrite(2, relay);
  
  if (!client.connected()) {
    stopClient(client);
  }

  delay(1000);
}

void stopClient(EthernetClient eClient) {
  Serial.println();
  Serial.println("Disconnecting");
  eClient.stop();
  while (true) {
    delay(25);
  }
}
