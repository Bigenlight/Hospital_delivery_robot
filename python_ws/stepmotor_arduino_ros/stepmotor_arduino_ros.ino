
int pos = 0;

//
int ENA = 2;
int IN1 = 8;
int IN2 = 9;
int ENB = 5;
int IN3 = 10;
int IN4 = 11;
int dtime = 11;

String order = "rest";
//
int i = 0;
unsigned long past = 0; // 과거 시간 저장 변수

void setup() {
  Serial.begin(9600);
  Serial.flush();
  
  pinMode(ENA, OUTPUT);
  pinMode(ENB, OUTPUT);
  pinMode(IN1, OUTPUT);
  pinMode(IN2, OUTPUT);
  pinMode(IN3, OUTPUT);
  pinMode(IN4, OUTPUT);
  digitalWrite(ENA, HIGH);
  digitalWrite(ENB, HIGH);
}

void clockwise()
{
  digitalWrite(IN1, LOW);
  digitalWrite(IN2, HIGH);
  digitalWrite(IN3, HIGH);
  digitalWrite(IN4, LOW);
  delay(dtime);


  digitalWrite(IN1, LOW);
  digitalWrite(IN2, HIGH);
  digitalWrite(IN3, LOW);
  digitalWrite(IN4, HIGH);
  delay(dtime);


  digitalWrite(IN1, HIGH);
  digitalWrite(IN2, LOW);
  digitalWrite(IN3, LOW);
  digitalWrite(IN4, HIGH);
  delay(dtime);


  digitalWrite(IN1, HIGH);
  digitalWrite(IN2, LOW);
  digitalWrite(IN3, HIGH);
  digitalWrite(IN4, LOW);
  delay(dtime);
}

void counter_clockwise()
{
  digitalWrite(IN1, HIGH);
  digitalWrite(IN2, LOW);
  digitalWrite(IN3, HIGH);
  digitalWrite(IN4, LOW);
  delay(dtime);


  digitalWrite(IN1, HIGH);
  digitalWrite(IN2, LOW);
  digitalWrite(IN3, LOW);
  digitalWrite(IN4, HIGH);
  delay(dtime);


  digitalWrite(IN1, LOW);
  digitalWrite(IN2, HIGH);
  digitalWrite(IN3, LOW);
  digitalWrite(IN4, HIGH);
  delay(dtime);


  digitalWrite(IN1, LOW);
  digitalWrite(IN2, HIGH);
  digitalWrite(IN3, HIGH);
  digitalWrite(IN4, LOW);
  delay(dtime);
}


void loop() {
  unsigned long now = millis();

  Serial.read();
  delay(100);
  

  if (Serial.available()) 
  {
    order = Serial.readStringUntil(' '); // Read a string until a newline character

    // Convert the string to an integer
    //order = input.toInt();

    while (Serial.available()) 
    {
      Serial.read(); // Clear any remaining characters in the serial buffer
    }
    past = now;
  }
  
  // 이전 명령이 현재와 일정 시간 초과시 명령 무효화
  if (now - past >= 3000)
    {
    order = "Rest";
    }
  
  Serial.print(order);
  Serial.print(", past: ");
  Serial.print(past);
  Serial.print(", now: ");
  Serial.print(now);
  Serial.print(", order: ");
  //Serial.println(order%30);

  if (order == "push" )
  {
    Serial.println("Moving Clockwise");
    digitalWrite(ENA, HIGH);
    digitalWrite(ENB, HIGH);
    while (i < 100)
    {
      clockwise();
      i++;
    }
    i = 0;
    delay(100);
  }

  else if (order == "pull" )
  {
    Serial.println("Moving Counter Clockwise");
    digitalWrite(ENA, HIGH);
    digitalWrite(ENB, HIGH);
    while (i < 100) {
      counter_clockwise();
      i++;
    }
    i = 0;
    delay(100);
  }

  else
  {
    Serial.println("resting");
    digitalWrite(ENA, LOW);
    digitalWrite(ENB, LOW);
  }
}
