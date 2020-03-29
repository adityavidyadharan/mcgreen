

#include <SR04.h>
#include <Wire.h>
#include <SPI.h>
#include <Adafruit_LIS3DH.h>
#include <Adafruit_Sensor.h>
//#define USE_USBCON
#include <ros.h>
#include <receiver/Peripheral.h> 
#include <receiver/Arm.h>
#include <motor_drive/Joystick.h>
#include <std_msgs/String.h>
#include <std_msgs/Int16.h>
//////////////////Ultrasonic
//Top Ultrasonic Pins
#define TRIG_PIN_t 6
#define ECHO_PIN_t 5
//Top Ultrasonic Pins
#define TRIG_PIN_b 4
#define ECHO_PIN_b 3

// Used for software SPI
#define LIS3DH_CLK 13
#define LIS3DH_MISO 12
#define LIS3DH_MOSI 11
// Used for hardware & software SPI
#define LIS3DH_CS 10


//SR04 sr04_t = SR04(ECHO_PIN_t, TRIG_PIN_t);
//SR04 sr04_b = SR04(ECHO_PIN_b, TRIG_PIN_b);
//////////////////Accel
Adafruit_LIS3DH lis = Adafruit_LIS3DH(LIS3DH_CS, LIS3DH_MOSI, LIS3DH_MISO, LIS3DH_CLK);

//////////////////ROS







ros::NodeHandle nh;
receiver::Arm data_msg;

ros::Publisher arm_pub("arduino_send", &data_msg);

// display a number on the digital segment display

void setup() 
{
  nh.initNode();
  nh.advertise(arm_pub);
  lis.begin(0x19);
  delay(1000);
  lis.setRange(LIS3DH_RANGE_4_G);   // 2, 4, 8 or 16 G!
  
}

long publisher_timer;

void loop()
{
  if (millis() > publisher_timer) {

      lis.read();
      data_msg.xyz_length=3;
      
      data_msg.xyz[0]=6.0;
      data_msg.xyz[1]=2.0;
      data_msg.xyz[2]=3.0;
      
     
      /*data_msg.xyz[0]=lis.x;
      data_msg.xyz[1]=lis.y;
      data_msg.xyz[2]=lis.z;
     */
      unsigned char side[6]="Right";
      data_msg.arm = side;
      //data_msg.top_sense = sr04_t.Distance();
      //data_msg.bottom_sense = sr04_b.Distance();
      arm_pub.publish(&data_msg);
    publisher_timer = millis() + 1000;

  }
  nh.spinOnce();
  //delay(50);
  
}
