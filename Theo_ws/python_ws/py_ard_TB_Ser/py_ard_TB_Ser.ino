#include <Servo.h>

Servo lefthand;
Servo righthand;

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
String arm_mode = "loading";
//
int i = 0;
unsigned long past = 0; // 과거 시간 저장 변수
unsigned long breaktime = 0;
//

void setup() 
{
  //
  Serial.begin(9600);
  Serial.flush();

  // Declare pins as output:
  pinMode(stepPin, OUTPUT);
  pinMode(dirPin, OUTPUT);

  righthand.attach(8);
  lefthand.attach(9);

  righthand.write(0);
  lefthand.write(180);
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
  righthand.write(0);
  lefthand.write(180);  
}

// Pushing
void counter_clockwise(int lap) 
{
  righthand.write(90);
  lefthand.write(90);
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
  
  //pull
  clockwise(rev);
}

void close_servo(){
  if(arm_mode == "loading"){
      Serial.print("loading: ");
      righthand.write(0);
      lefthand.write(180);
  }
  else Serial.print("unloading: ");
}

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

  // 이전 명령이 현재와 일정 시간 초과시 명령 무효화
  if (now - past >= 3000)
  {
    order = "nomsg";
  }

  // 시리얼 메시지 전송 
  Serial.print("receive: ");
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

  if (now - breaktime <= 10000)
  {
    order = "rest";
    Serial.print("break time");
  }
  

  if(order == "lo") arm_mode = "loading";
  if(order == "o") arm_mode = "loading";
  if(order == "olo") arm_mode = "loading";
  if(order == "un") arm_mode = "unloading";
  if(order == "n") arm_mode = "unloading";
  if(order == "nun") arm_mode = "unloading";


  // 명령
  if (now - breaktime <= 10000)
  {
    order = "rest";
    Serial.print("break time");
  } 
  else if (order == "push" && state == "pulled")
  {
    // Set the spinning direction counterclockwise:
    digitalWrite(dirPin, LOW);
    Serial.println("Moving Counter Clockwise");
    counter_clockwise(rev);
    breaktime = now;
    delay(100);
  }
  else if (order == "ush" && state == "pulled")
  {
    // Set the spinning direction counterclockwise:
    digitalWrite(dirPin, LOW);
    Serial.println("Moving Counter Clockwise");
    counter_clockwise(rev);
    breaktime = now;
    delay(100);
  }

//  else if (order == "pull" && state == "pushed")
//  {
//    // Set the spinning direction clockwise:
//    digitalWrite(dirPin, HIGH);
//    Serial.println("Moving Clockwise");
//    clockwise(rev);
//    state = "pulled";
//    delay(100);
//  }
//  else if (order == "ull" && state == "pushed")
//  {
//    // Set the spinning direction clockwise:
//    digitalWrite(dirPin, HIGH);
//    Serial.println("Moving Clockwise");
//    clockwise(rev);
//    state = "pulled";
//    delay(100);
//  }

  else
  {
    Serial.println("resting");
  }
}
