char cmd;
#include <Servo.h>                   
Servo myservo;
int pos = 0;       
int destination = 0;

int servoPin = 6;

void setup() {
  Serial.begin(9600);
  
  pinMode (servoPin, OUTPUT);
  myservo.attach(6);
}

void loop() {

  // 컴퓨터로부터 시리얼 통신이 전송되면, 한줄씩 읽어와서 cmd 변수에 입력
  if(Serial.available()){
    cmd = Serial.read();
    destination = cmd - '0'; 
    for (pos = 0; pos <= destination; pos += 1)
    {
    myservo.write(pos);
    delay(100);                                         

    }

    for (pos = destination; pos >= 0; pos -= 1)    // pos가 180이면, 0도보다 크다면 , 1도씩 빼라
    {
    myservo.write(pos);                           // 서보모터를 pos 각도로 움직여라 

    delay(100);                                        // 0.1초의 딜레이 ( 1초 = 1000 )
    } 

    
    Serial.print("아두이노: ");
    Serial.println(cmd);
    delay(100);

  }
}
