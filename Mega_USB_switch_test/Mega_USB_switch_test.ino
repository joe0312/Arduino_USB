//Mega USB switch test
 	
const int conPin = 40;


void setup() {
  pinMode(conPin, OUTPUT); 
}

void loop() {
  analogWrite(conPin, 255);
}
