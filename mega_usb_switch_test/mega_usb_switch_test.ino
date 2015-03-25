//Mega USB switch test

char incomingByte = 0; 
const int conPin = 40;

void setup() {
  pinMode(conPin, OUTPUT);
  Serial.begin(115200);
  Serial.println("Connecting to USB(YorN)??");
}

void loop() {
  while (Serial.available() > 0) {
    incomingByte = Serial.read();
    Serial.print("Connect received: ");
    Serial.println(incomingByte);
  }
  
  if (incomingByte == 'Y'){
    analogWrite(conPin, 255);
  }
  else if(incomingByte == 'N'){
    analogWrite(conPin, 0);
  }
}
