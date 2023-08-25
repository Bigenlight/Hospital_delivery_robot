int ENA=2;
int IN1=8;
int IN2=9;
int ENB=5;
int IN3=10;
int IN4=11;
int dtime = 11;
int i =0;

int direction = 0;


void setup()
{
Serial.begin(9600);
  
 pinMode(ENA,OUTPUT);
 pinMode(ENB,OUTPUT);
 pinMode(IN1,OUTPUT);
 pinMode(IN2,OUTPUT);
 pinMode(IN3,OUTPUT);
 pinMode(IN4,OUTPUT);
 digitalWrite(ENA,HIGH);
 digitalWrite(ENB,HIGH);
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

void loop()
{
  if(Serial.available()){
    direction = Serial.parseInt();
    
  }
  Serial.println(direction);
  
  if (direction == 1)
  {
    Serial.println("Moving Clockwise");
    digitalWrite(ENA, HIGH);
    digitalWrite(ENB, HIGH);
    while (i < 160)
    {
      clockwise();
      i++;
    }
    i = 0;
    delay(100);
  }
  else if (direction == 2)
  {
    Serial.println("Moving Counter Clockwise");
    digitalWrite(ENA, HIGH);
    digitalWrite(ENB, HIGH);
    while (i < 160) {
      counter_clockwise();
      i++;
    }
    i = 0;
    delay(100);
  }
  
//  if(direction == 0){
//    //clockwise
// digitalWrite(IN1,LOW);
// digitalWrite(IN2,HIGH);
// digitalWrite(IN3,HIGH);
// digitalWrite(IN4,LOW);
// delay(dtime);
//
//
// digitalWrite(IN1,LOW);
// digitalWrite(IN2,HIGH);
// digitalWrite(IN3,LOW);
// digitalWrite(IN4,HIGH);
// delay(dtime);
//
//
// digitalWrite(IN1,HIGH);
// digitalWrite(IN2,LOW);
// digitalWrite(IN3,LOW);
// digitalWrite(IN4,HIGH);
// delay(dtime);
//
//
// digitalWrite(IN1,HIGH);
// digitalWrite(IN2,LOW);
// digitalWrite(IN3,HIGH);
// digitalWrite(IN4,LOW);
// delay(dtime);
//  }
//
//
//  if(direction == 1){
//    //counter clockwise
// digitalWrite(IN1,HIGH);
// digitalWrite(IN2,LOW);
// digitalWrite(IN3,HIGH);
// digitalWrite(IN4,LOW);
// delay(dtime);
//
//
// digitalWrite(IN1,HIGH);
// digitalWrite(IN2,LOW);
// digitalWrite(IN3,LOW);
// digitalWrite(IN4,HIGH);
// delay(dtime);
//
//
// digitalWrite(IN1,LOW);
// digitalWrite(IN2,HIGH);
// digitalWrite(IN3,LOW);
// digitalWrite(IN4,HIGH);
// delay(dtime);
//
//
// digitalWrite(IN1,LOW);
// digitalWrite(IN2,HIGH);
// digitalWrite(IN3,HIGH);
// digitalWrite(IN4,LOW);
// delay(dtime);
//  }


}
