
int rev = 3;
//
int pos = 0;
#define dirPin 2
#define stepPin 3
#define stepsPerRevolution 1300
#define dtime 1000
//
String order = "rest";
String state = "pulled";
//
int i = 0;
unsigned long past = 0; // 과거 시간 저장 변수
//

void setup() {
  Serial.begin(1000000);
  Serial.flush();

  // Declare pins as output:
  pinMode(stepPin, OUTPUT);
  pinMode(dirPin, OUTPUT);
}

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
}

void counter_clockwise(int lap) 
{
  // Spin the stepper motor 1 revolution quickly:
  for (int i = 0; i < lap * stepsPerRevolution; i++) {
    // These four lines result in 1 step:
    digitalWrite(stepPin, HIGH);
    delayMicroseconds(dtime);
    digitalWrite(stepPin, LOW);
    delayMicroseconds(dtime);
  }
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
  Serial.print(", state: ");
  Serial.print(state);
  Serial.print(", order: ");
  

  // 명령 
  if (order == "push" && state == "pulled")
  {
    // Set the spinning direction clockwise:
    digitalWrite(dirPin, HIGH);
    Serial.println("Moving Clockwise");
    clockwise(rev);
    state = "pushed";
    delay(100);
  }

  else if (order == "pull" && state == "pushed")
  {
    // Set the spinning direction counterclockwise:
    digitalWrite(dirPin, LOW);
    Serial.println("Moving Counter Clockwise");
    counter_clockwise(rev);
    state = "pulled";
    delay(100);
  }

  else
  {
    Serial.println("resting");
  }
}
