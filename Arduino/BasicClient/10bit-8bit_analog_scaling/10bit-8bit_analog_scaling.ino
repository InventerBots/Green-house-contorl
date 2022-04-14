const float scale = 0.24926686217008797653958944281525;
void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);
  pinMode(A0, INPUT);
}

void loop() {
  short int a = 512*(255/1023);
  int scaled (analogRead(A0)*scale);
  Serial.println(scaled);
  Serial.println(analogRead(A0));
  delay(50);
}
