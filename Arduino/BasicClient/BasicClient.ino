#include <SPI.h>
#include <Ethernet.h>

#define NUM_SESNSOR 3

int tempF;

byte mac[] = { 0xA6, 0x61, 0x0A, 0xAE, 0x74, 0x86 };
int port = 10004;

bool startUp = true;

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
  // while (!Serial) {
  //   ;
  // }

  Serial.println("Serial started");

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
}

void loop() {
  // store all three sesnors in one array
  int sensorVal[3] = {analogRead(A0), analogRead(A1), analogRead(A2)};
  
  float tempRaw = analogRead(A0);
  
  Serial.println(tempRaw);

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
