#include <SPI.h>
#include <Ethernet.h>

uint8_t mac[] = { 0xA6, 0x61, 0x0A, 0xAE, 0x74, 0x86 };
int port = 10004;

IPAddress ip(192, 168, 1, 178);
IPAddress server(192, 168, 1, 220);  // RPi ip is 192.168.1.220

EthernetClient client;

const uint8_t thermister_0 = A0;
const uint8_t thermister_1 = A1;
const uint8_t thermister_2 = A2;
const uint8_t thermister_3 = A3;
const uint8_t thermister_outside = A4;

void setup() {
  Serial.begin(115200);
  while (!Serial) {  // wait for serial port to open
    ;
  }
  Serial.println("serial is running");

  Ethernet.init(10);        // use pin 10 for chip slect
  Ethernet.begin(mac, ip);  // start ethernet socket

  analogReadResolution(12); // manualy set ADC resolution to 12 bit
  pinMode(thermister_0, INPUT);
  pinMode(thermister_1, INPUT);
  pinMode(thermister_2, INPUT);

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
      delay(3000);  // wait 3 secconds before trying to connect again
    }
  }
}

void loop() {
  int sensorVal[] = {
    (int)analogRead(thermister_0),
    (int)analogRead(thermister_1),
    (int)analogRead(thermister_2),
    (int)analogRead(thermister_3),
    (int)analogRead(thermister_outside)
  };

  int data = 0;
  int dataCach = 0;
  int error = 0;
  
  if (client.available()) {
    if (error == 0) {  // if no error is present update data
      data = client.read();
      if (data > 0) {
        dataCach = data - 1;
      }
      // Serial.print("No error detected, recived index: ");
      Serial.println(dataCach);
    }
    if (data > 0 || error != 0) {
      Serial.print("sending: ");
      Serial.println(sensorVal[dataCach]);
      client.print(sensorVal[dataCach]);
      data = 0;  // reset data to prevent spamming server
    }
  }

  client.flush();

  if (!client.connected()) {
    client.stop();
    Serial.println("Server disconnected, restarting");
    delay(5000);
    setup();
  }
}