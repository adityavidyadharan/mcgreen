#include <SR04.h>
//#include <FlySkyIBus.h>
#include <ros.h>
#include <receiver/Peripheral.h> 
#include <motor_drive/Joystick.h>
#include <std_msgs/String.h>
#include <std_msgs/Int16.h>
//Ultrasonic Pins
#define TRIG_PIN 22
#define ECHO_PIN 24
//Seven Seg Pins
/*
#define A_PIN 30
#define B_PIN 32
#define C_PIN 34
#define D_PIN 36
#define E_PIN 38
#define F_PIN 40
#define G_PIN 42
*/
SR04 sr04 = SR04(ECHO_PIN, TRIG_PIN);
byte seven_seg_digits[10] = { B1111110,  // = 0
                              B0110000,  // = 1
                              B1101101,  // = 2
                              B1111001,  // = 3
                              B0110011,  // = 4
                              B1011011,  // = 5
                              B1011111,  // = 6
                              B1110000,  // = 7
                              B1111111,  // = 8
                              B1110011   // = 9
                             }; 
 
ros::NodeHandle nh;
receiver::Peripheral ultra_msg;

ros::Publisher ultra_pub("arduino_send", &ultra_msg);


void status_update(const motor_drive::Joystick& seg_number)
{
  
  for (int i = 0; i < 7; i++)
  {
    digitalWrite(i*2+30, bitRead((int)(seven_seg_digits[seg_number.joy[0]]), 6-i));
  }
  if (seg_number.joy[1] == 1)
  {
    digitalWrite(52, LOW);
  }
  if (seg_number.joy[1] == 0)
  {
    digitalWrite(52, HIGH);
  }
}

ros::Subscriber<motor_drive::Joystick> status_sub("LED_control", &status_update);

void setup() 
{
  nh.initNode();
  nh.subscribe(status_sub);
  nh.advertise(ultra_pub);
  pinMode(13, OUTPUT);
  pinMode(52, OUTPUT);
  for (int i = 30; i <= 42; i+=2)
  {
    pinMode(i, OUTPUT);
  }
  digitalWrite(13, HIGH);
  pinMode(TRIG_PIN, OUTPUT);
  pinMode(ECHO_PIN, INPUT);
}

void loop()
{
  ultra_msg.us=sr04.Distance();
  if (ultra_msg.us == 0)
  {
    digitalWrite(13, HIGH);
  }
  else
  {
    digitalWrite(13, LOW);
  }
  ultra_pub.publish(&ultra_msg);
  //delay(500);
  nh.spinOnce();
}
