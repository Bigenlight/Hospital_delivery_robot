int32_t order = 5;
void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  Serial.flush();
}

void loop() {
  // put your main code here, to run repeatedly:
  if (Serial.available()>= 4)
  {
    //order = Serial.read(); // Read a string until a newline character

    // Convert the string to an integer
    //order = input.toInt();

    //while (Serial.available())
    //{
    // Serial.read(); // Clear any remaining characters in the serial buffer
    //}
    //Serial.read();

    // Read the int32 value as a byte array
    Serial.readBytes((char*)&order, 4);


    //while (Serial.available())
    //{
    // Serial.read(); // Clear any remaining characters in the serial buffer
    //}
    //Serial.read();

    
  }
  //Serial.read();
  //Serial.print("receive:");
    Serial.print(order);
    //Serial.print(" ");
}
