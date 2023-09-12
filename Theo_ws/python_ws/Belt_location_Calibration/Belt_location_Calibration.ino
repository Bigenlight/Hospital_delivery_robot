#define dirPin 2
#define stepPin 3
#define stepsPerRevolution 100
#define dtime 1000

int number = 0;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  Serial.flush();

  // Declare pins as output:
  pinMode(stepPin, OUTPUT);
  pinMode(dirPin, OUTPUT);
}

// Pulling
void clockwise(int lap) 
{
  digitalWrite(dirPin, HIGH);
  // Spin the stepper motor 1 revolution slowly:
  for (int i = 0; i < lap * stepsPerRevolution; i++) {
    // These four lines result in 1 step:
    digitalWrite(stepPin, HIGH);
    delayMicroseconds(dtime);
    digitalWrite(stepPin, LOW);
    delayMicroseconds(dtime);
  }
}

// Pushing
void counter_clockwise(int lap) 
{
  digitalWrite(dirPin, LOW);
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
   if (Serial.available())
  {
    String order = Serial.readStringUntil(' ');

    if(order == "push"){
      Serial.println("prepare to push");
      while(true){
        if (Serial.available())
        {
          number  = Serial.parseInt();
          if(number == 0) {
            Serial.println("break");
            break;
          }
          
          counter_clockwise(number) ;
          Serial.read();
        }
      }
    }

    if(order == "pull"){
      Serial.println("prepare to pull");
      while(true){
        if (Serial.available())
        {
          number  = Serial.parseInt();
          if(number == 0) {
            Serial.println("break"); 
            break;}
          
          clockwise(number) ;
          Serial.read();
        }
      }

    }
    Serial.read();
    }
  }


