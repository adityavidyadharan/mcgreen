#include <SR04.h>
#include <ros.h>
//#include <motor_drive/Peripheral.h>
#include <node_control/Array.h>
#include <std_msgs/String.h>
#include <std_msgs/Int16.h>

//int channels[10] = {1000, 2000, 1500, 1500, 0, 0, 0, 0, 0, 0};
int joy_l[4];
int joy_r[4];

ros::NodeHandle nh;


void status_update(const node_control::Array& motors)
{

  if (motors.arr[0] < 1250) {
    digitalWrite(13, LOW);
  }
  if (motors.arr[0] > 1750) {
    digitalWrite(13, HIGH);
  }
  joy_l[0] = motors.arr[0];   // Map controller inputs to a different array, idk why
  joy_l[1] = motors.arr[1];
  joy_r[0] = motors.arr[2];
  joy_r[1] = motors.arr[3];

  // Use left joystick for direction control

  if (joy_l[1] > 1500) {
    digitalWrite(22, HIGH);               // Left Motor
    digitalWrite(23, LOW);
    digitalWrite(24, HIGH);               // Right Motor
    digitalWrite(25, LOW);
  }
  else if (joy_l[1] < 1500) {
    digitalWrite(22, LOW);
    digitalWrite(23, HIGH);
    digitalWrite(24, LOW);
    digitalWrite(25, HIGH);
  }
  else {
    digitalWrite(22, LOW);
    digitalWrite(23, LOW);
    digitalWrite(24, LOW);
    digitalWrite(25, LOW);
  }

  // Use right joystick for speed control

  int max_speed;
  if (joy_l[1] > 1500) {
    max_speed = map(joy_l[1], 1500, 2000, 0, 255);
  }
  else {
    max_speed = map(joy_l[1], 1500, 1000, 0, 255);
  }

  if (joy_r[0] > 1500) {
    int speed_r = map(joy_r[0], 2000, 1500, 0, max_speed);
    analogWrite(9, speed_r);                     // Right Motor
    analogWrite(10, max_speed);                     // Left Motor
  }
  else if (joy_r[0] < 1500) {
    int speed_l = map(joy_r[0], 1000, 1500, 0, max_speed);
    analogWrite(9, max_speed);
    analogWrite(10, speed_l);
  }
  else {
    analogWrite(9, max_speed);
    analogWrite(10, max_speed);
  }

  // delay(200);
}



ros::Subscriber<node_control::Array> status_sub("/lower_safety", &status_update);



void setup() {
  pinMode(9, OUTPUT);
  pinMode(10, OUTPUT);
  pinMode(22, OUTPUT);
  pinMode(23, OUTPUT);
  pinMode(24, OUTPUT);
  pinMode(25, OUTPUT);
  pinMode(13, OUTPUT);
                nh.initNode();
                nh.subscribe(status_sub);
                //Serial2.begin(115200);


}







void loop() {

  /*if (channels[1] > 1000){
    channels[1] -= 20;
    }

    joy_l[0] = channels[0];   // Map controller inputs to a different array, idk why
    joy_l[1] = channels[1];
    joy_r[0] = channels[2];
    joy_r[1] = channels[3];

    // Use left joystick for direction control

    if (joy_l[1] > 1500){
    digitalWrite(22, HIGH);               // Left Motor
    digitalWrite(23, LOW);
    digitalWrite(24, HIGH);               // Right Motor
    digitalWrite(25, LOW);
    }
    else if (joy_l[1] < 1500) {
    digitalWrite(22, LOW);
    digitalWrite(23, HIGH);
    digitalWrite(24, LOW);
    digitalWrite(25, HIGH);
    }
    else {
    digitalWrite(22, LOW);
    digitalWrite(23, LOW);
    digitalWrite(24, LOW);
    digitalWrite(25, LOW);
    }

    // Use right joystick for speed control

    int max_speed;
    if (joy_l[1] > 1500){
    max_speed = map(joy_l[1], 1500, 2000, 0, 255);
    }
    else{
    max_speed = map(joy_l[1], 1500, 1000, 0, 255);
    }

    if (joy_r[0] > 1500){
    int speed_r = (1500-(((joy_r[0] - 1500)/500)))*max_speed;
    analogWrite(9, speed_r);                     // Right Motor
    analogWrite(10, max_speed);                     // Left Motor
    }
    else if (joy_r[0] < 1500) {
    int speed_l = (1500-(abs(joy_r[0] - 1500)/500))*max_speed;
    analogWrite(9, max_speed);
    analogWrite(10, speed_l);
    }
    else {
    analogWrite(9, max_speed);
    analogWrite(10, max_speed);
    }

    delay(200);*/
  nh.spinOnce();
  //delay(1);

}
