//*******************************************************************************
// Project : Buzzer 
// Board : Arduino Uno  + easy shield board
// By : Kit Plus
//*******************************************************************************/
// Define Pins
#define BUZZER 13
#define BUTTON 4
#define NOTE_C5  523
#define NOTE_CS5 554
#define NOTE_D5  587
#define NOTE_DS5 622
#define NOTE_E5  659
#define NOTE_F5  698
#define NOTE_FS5 740
#define NOTE_G5  784
#define NOTE_GS5 831
#define NOTE_A5  880
#define NOTE_AS5 932
#define NOTE_B5  988
#define NOTE_C6  1047
int melody[] = {
  NOTE_C5, NOTE_D5, NOTE_E5, NOTE_F5, NOTE_G5, NOTE_A5, NOTE_B5, NOTE_C6};
int duration = 500;  // 500 miliseconds
 
void setup() {
 
}
 
void loop() {  
  // 도레미파솔라시도
  for (int thisNote = 0; thisNote < 8; thisNote++) {
    tone(BUZZER, melody[thisNote], duration);
    delay(1000);
  }
   
  delay(1000);
}
