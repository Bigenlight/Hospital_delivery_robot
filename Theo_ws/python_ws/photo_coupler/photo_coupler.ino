int led = 7;
int Photo = A0;
 
void setup(){
    Serial.begin(9600);       // 시리얼 모니터 시작, 속도는 9600
    pinMode(led, OUTPUT);
    pinMode(Photo, INPUT);
}
void loop(){
    int val = digitalRead(Photo);  // 포토 인터럽터 스위치에서 데이터 읽어오기
    Serial.println(val);
    
    if( val != 1 ) //물체가 감지 안되면 led off
      digitalWrite(led, HIGH);
    else //감지되면 led on
      digitalWrite(led, LOW);
   
    delay(100);
}
