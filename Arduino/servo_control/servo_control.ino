//ROS SETUP
#include <ros.h>
#include <node_control/Array.h>
ros::NodeHandle_<ArduinoHardware, 2, 2, 80, 105> nh;

//Servo Setup
#include <Servo.h>
#define servoVert 3
#define servoHoriz 4
#define modifier 180
//#define USE_USBCON
Servo ServoUD;
Servo ServoLR;
int vertPos = 90;
int horizPos = 90;

//ROS Callback
//servos.arr[0] = Vertical movement
//servos.arr[1] = Horizontal movement
void servo_callback(const node_control::Array& servos);

ros::Subscriber<node_control::Array> servo_sub("/upper_safety", &servo_callback);
void setup() {
   ServoUD.attach(servoVert);
   ServoLR.attach(servoHoriz);
   ServoUD.write(vertPos);
   ServoLR.write(horizPos);
   
   nh.initNode();
   nh.subscribe(servo_sub);
   
   pinMode(13, OUTPUT);
   digitalWrite(13, LOW);
}
void loop(){
    nh.spinOnce();
}

void servo_callback(const node_control::Array& servos)
{
    int speed = map(servos.arr[0], 1000, 2000, 0, modifier);
    //speed = speed + vertPos;
    //vertPos=speed;
    ServoUD.write(speed);
    speed = map(servos.arr[1], 1000, 2000, 0, modifier);
    //speed = speed + horizPos;
    //horizPos=speed;
    ServoLR.write(speed);
}
