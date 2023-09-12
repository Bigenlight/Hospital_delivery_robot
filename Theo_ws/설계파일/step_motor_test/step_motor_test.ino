int ENA=2;
int IN1=8;
int IN2=9;
int ENB=5;
int IN3=10;
int IN4=11;
int dtime = 11;

bool direction = false;

void setup()
{
 pinMode(ENA,OUTPUT);
 pinMode(ENB,OUTPUT);
 pinMode(IN1,OUTPUT);
 pinMode(IN2,OUTPUT);
 pinMode(IN3,OUTPUT);
 pinMode(IN4,OUTPUT);
 digitalWrite(ENA,HIGH);
 digitalWrite(ENB,HIGH);
}

void loop()
{
  if(direction == true){ 
    //clockwise
 digitalWrite(IN1,LOW);
 digitalWrite(IN2,HIGH);
 digitalWrite(IN3,HIGH);
 digitalWrite(IN4,LOW);
 delay(dtime);

 digitalWrite(IN1,LOW);
 digitalWrite(IN2,HIGH);
 digitalWrite(IN3,LOW);
 digitalWrite(IN4,HIGH);
 delay(dtime);

 digitalWrite(IN1,HIGH);
 digitalWrite(IN2,LOW);
 digitalWrite(IN3,LOW);
 digitalWrite(IN4,HIGH);
 delay(dtime);

 digitalWrite(IN1,HIGH);
 digitalWrite(IN2,LOW);
 digitalWrite(IN3,HIGH);
 digitalWrite(IN4,LOW);
 delay(dtime);
  }

  if(direction == false){
    //counter clockwise
 digitalWrite(IN1,HIGH);
 digitalWrite(IN2,LOW);
 digitalWrite(IN3,HIGH);
 digitalWrite(IN4,LOW);
 delay(dtime);

 digitalWrite(IN1,HIGH);
 digitalWrite(IN2,LOW);
 digitalWrite(IN3,LOW);
 digitalWrite(IN4,HIGH);
 delay(dtime);

 digitalWrite(IN1,LOW);
 digitalWrite(IN2,HIGH);
 digitalWrite(IN3,LOW);
 digitalWrite(IN4,HIGH);
 delay(dtime);

 digitalWrite(IN1,LOW);
 digitalWrite(IN2,HIGH);
 digitalWrite(IN3,HIGH);
 digitalWrite(IN4,LOW);
 delay(dtime);
  }

}

