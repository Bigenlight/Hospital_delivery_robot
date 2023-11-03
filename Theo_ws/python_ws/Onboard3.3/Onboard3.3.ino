#include <Servo.h>
//#include <toneAC.h>


Servo lefthand;
Servo righthand;

#define rclose 27
#define lclose 170
#define ropen 130
#define lopen 70
#define half_rclose 55
#define half_lclose 140

int rev = 1;
//
int pos = 0;
#define dirPin 2
#define stepPin 3
#define stepsPerRevolution 1300
#define dtime 1000
//
String order = "rest";
String state = "pulled";
String arm_mode = "unloading"; // 기본이 배송으로
bool half_closed = false;
bool mission = false;// 미션수행 여부(false는 안한)
//
int i = 0;
unsigned long past = 0; // 과거 시간 저장 변수
long breaktime = -15000;
// 부
int speakerPin = 13;
long bpast = 0;
//

void setup()
{
  //
  Serial.begin(300);
  Serial.flush();

  // Declare pins as output:
  pinMode(stepPin, OUTPUT);
  pinMode(dirPin, OUTPUT);

  righthand.attach(8);
  lefthand.attach(9);

  righthand.write(rclose);
  lefthand.write(lclose);
}

// Pulling
void clockwise(int lap)
{
  // Spin the stepper motor 1 revolution slowly:
  for (int i = 0; i < lap * stepsPerRevolution; i++) {
    // These four lines result in 1 step:
    digitalWrite(stepPin, HIGH);
    delayMicroseconds(dtime);
    digitalWrite(stepPin, LOW);
    delayMicroseconds(dtime);
  }
  state = "pulled";
  //righthand.write(rclose);
  //lefthand.write(lclose);
  closing_arm();

  mission= true;
}
void closing_arm(){

  if(arm_mode = "unloading"){
    righthand.write(half_rclose);
    lefthand.write(half_lclose);
    half_closed = true;
  }
  else{
    righthand.write(rclose);
    lefthand.write(lclose);
  }
}

// Pushing
void counter_clockwise(int lap)
{
  // open servo
  righthand.write(ropen);
  lefthand.write(lopen);
  delay(500);
  // Spin the stepper motor 1 revolution quickly:
  for (int i = 0; i < lap * stepsPerRevolution; i++) {
    // These four lines result in 1 step:
    digitalWrite(stepPin, HIGH);
    delayMicroseconds(dtime);
    digitalWrite(stepPin, LOW);
    delayMicroseconds(dtime);
  }
  close_servo();
  state = "pushed";
  delay(100);
  //pull
  Serial.println("Moving Clockwise");
  digitalWrite(dirPin, HIGH);
  clockwise(rev);
}

void close_servo() {
  if (arm_mode == "loading") { // 모드 
    Serial.print("loading: ");
    righthand.write(rclose);
    lefthand.write(lclose);
    delay(1000);
  }
  else Serial.print("unloading: ");
}

void alarm(int y) 
{
  int j = 0;
  Serial.println("emergency");

  if(bpast > millis() - 15000 && bpast != 0) return;

  while (j < y) 
  {
    tone(speakerPin, 800);
    delay(500);
    tone(speakerPin, 500);
    delay(500);
    noTone(speakerPin);
    Serial.print("emergency ");
    Serial.println(j);
    j = j + 1;
  }
  
  order = "rest";
  state = "alarm";
  bpast = millis();
}


//////////////////////////////////////////////////////////////////////////////////
void loop() {
  unsigned long now = millis();

  // Serial.read();
  //  delay(100);
  if (Serial.available())
  {
    order = Serial.readStringUntil(' '); // Read a string until a newline character

    // Convert the string to an integer
    //order = input.toInt();

    //    while (Serial.available())
    //    {
    //      Serial.read(); // Clear any remaining characters in the serial buffer
    //    }
    Serial.read();

    past = now;
  }
 // else {Serial.print("NNO");return;}

  //복귀 감지 
  if(mission == true){
    //for(int k =0 ;k < 20; k++){
      Serial.println("return ");
      delay(100);
      //}
      mission = false;
      return;
    }

  // 부저알람
  if (order == "per")alarm(10);
  else if (order == "er") alarm(10);
  else if (order == " r") alarm(10);

  
  // 이전 명령이 현재와 일정 시간 초과시 명령 무효화
//  if (now - past >= 3000)
//  {
//    order = "nomsg";
//  }


  if (order == "lo") arm_mode = "loading";
  else if (order == "o") arm_mode = "loading";
  else if (order == " o") arm_mode = "loading";
  else if (order == "olo") arm_mode = "loading";
  else if (order == "un") arm_mode = "unloading";
  else if (order == "n") arm_mode = "unloading";
  else if (order == " n") arm_mode = "unloading";
  else if (order == "nun") arm_mode = "unloading";

  if (now - breaktime <= 30000)
  {
    order = "justdone";
    Serial.println("break time ");
  }
  if(half_closed == true && now - breaktime >= 20000){
      half_closed == false;
      close_servo();
    }


  // 명령
 if (order == "push" || order == " push" ||order == "ush" || order == "push " || order == " push " )
  {
    // Set the spinning direction counterclockwise:
    digitalWrite(dirPin, LOW);
    Serial.println("Moving Counter Clockwise");
    counter_clockwise(rev);
    breaktime = now;
    delay(100);
  }
//  else if (order == "ush" && state == "pulled")
//  {
//    // Set the spinning direction counterclockwise:
//    digitalWrite(dirPin, LOW);
//    Serial.println("Moving Counter Clockwise");
//    counter_clockwise(rev);
//    breaktime = now;
//    delay(100);
//  }
  
  else
  {
    Serial.println("resting ");
  }
  
  // 시리얼 메시지 전송
  Serial.print(" /Receive: ");
  Serial.print(order);
  Serial.print(", past: ");
  Serial.print(past);
  Serial.print(", now: ");
  Serial.print(now);
  Serial.print(", bt: ");
  Serial.print(breaktime);
  Serial.print(", state: ");
  Serial.print(state);
  Serial.print(", mode: ");
  Serial.print(arm_mode);
  Serial.println(", behave: ");

  order="NoNewOrder";
}
