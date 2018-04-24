/*
 * CODE: get commands to control the bot from
 *      the bluetooth and then execute the command
 *      operations accprdingly.
 */

#define IN_11  2                // L298N #1 in 1 motor Front Right
#define IN_12  3                // L298N #1 in 2 motor Front Right
#define IN_13  4                // L298N #1 in 3 motor Back Right
#define IN_14  7                // L298N #1 in 4 motor Back Right

#define IN_21  8                // L298N #2 in 1 motor Front Left
#define IN_22  9                // L298N #2 in 2 motor Front Left
#define IN_23  12               // L298N #2 in 3 motor Back Left
#define IN_24  13               // L298N #2 in 4 motor Back Left

void setup() {  
        pinMode(IN_11, OUTPUT);
        pinMode(IN_12, OUTPUT);
        pinMode(IN_13, OUTPUT);
        pinMode(IN_14, OUTPUT);
        pinMode(IN_21, OUTPUT);
        pinMode(IN_22, OUTPUT);
        pinMode(IN_23, OUTPUT);
        pinMode(IN_24, OUTPUT);
        pinMode(10, OUTPUT);
        Serial.begin(9600); 
} 

void goAhead(){ 
        digitalWrite(IN_11, HIGH);
        digitalWrite(IN_12, LOW);
        digitalWrite(IN_13, LOW);
        digitalWrite(IN_14, HIGH);
        digitalWrite(IN_21, LOW);
        digitalWrite(IN_22, HIGH);
        digitalWrite(IN_23, HIGH);
        digitalWrite(IN_24, LOW);
}

void goLeft(){
        digitalWrite(IN_11, HIGH);
        digitalWrite(IN_12, LOW);
        digitalWrite(IN_13, LOW);
        digitalWrite(IN_14, HIGH);
        digitalWrite(IN_21, HIGH);
        digitalWrite(IN_22, LOW);      
        digitalWrite(IN_23, LOW);
        digitalWrite(IN_24, HIGH);
}

void stopRobot(){  
        digitalWrite(IN_11, LOW);
        digitalWrite(IN_12, LOW);
        digitalWrite(IN_13, LOW);
        digitalWrite(IN_14, LOW);
        digitalWrite(IN_21, LOW);
        digitalWrite(IN_22, LOW);
        digitalWrite(IN_23, LOW);
        digitalWrite(IN_24, LOW);
}
  
void loop(){
        digitalWrite(10, HIGH);
        if (Serial.available() > 0) {
                char data = Serial.read();
                Serial.write(data);
                switch (data) {
                        case 'F':goAhead();break;
                        case 'L':goLeft();break;
                        case 'S': stopRobot(); break;
        
                }
        }
}
