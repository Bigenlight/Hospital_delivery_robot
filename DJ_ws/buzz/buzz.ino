int speakerPin = 13;


void setup() {

}

 

void loop() {
  buzzEmergency();
}

void buzzEmergency(){
  tone(speakerPin, 800);
  delay(500);
  tone(speakerPin, 500);
  delay(500);
  noTone(speakerPin);
}
