//I took out my testing code and i left just the expressions 
#include <LedControl.h>
#include <ros.h>
#include <node_control/Face.h>
#include <std_msgs/String.h>
#include <std_msgs/Int16.h>
//12, 11 and 10 are the pins I used, but you can change them here 
//--> only place where you need to change them
LedControl lc = LedControl(12, 10, 11, 7);
ros::NodeHandle nh; 

/*
-3=sad3
-2=sad2
-1=sad1
0=neutral
1=happy1
2=happy2
3=happy3
8=surp
9=blink
10=safety
*/
void face_callback(const node_control::Face& msg)
{
  switch(msg.Expression)
  {
    case -3: sad3();
    break;
    case -2: sad2();
    break;
    case -1: sad1();
    break;
    case 0: neutral();
    break;
    case 1: happy1();
    break;
    case 2: happy2();
    break;
    case 3: happy3();
    break;
    case 9: surp();
    break;
    case 10: _blink();
    break;
  }
  //add code to change color
  
}
ros::Subscriber<node_control::Face> face_sub("dot_matrix_send", &face_callback);
void setup() {
  
  //initialize ros
  nh.initNode();
  nh.subscribe(face_sub);
  delay(100);
  
  lc.shutdown(0, false);
  lc.setIntensity(0, 1);
  lc.clearDisplay(0);

  lc.shutdown(1, false);
  lc.setIntensity(1, 1);
  lc.clearDisplay(1);

  lc.shutdown(2, false);
  lc.setIntensity(2, 1);
  lc.clearDisplay(2);

  lc.shutdown(3, false);
  lc.setIntensity(3, 1);
  lc.clearDisplay(3);

  lc.shutdown(4, false);
  lc.setIntensity(4, 1);
  lc.clearDisplay(4);

  lc.shutdown(5, false);
  lc.setIntensity(5, 1);
  lc.clearDisplay(5);

  lc.shutdown(6, false);
  lc.setIntensity(6, 1);
  lc.clearDisplay(6);

}

void loop() {
 nh.spinOnce();
}

//Eyes open happy closed mouth
void neutral() {
  lc.setRow(0, 5, 7);
  lc.setRow(0, 6, 15);
  lc.setRow(0, 7, 15);
  lc.setRow(1, 5, 129);
  lc.setRow(1, 6, 195);
  lc.setRow(1, 7, 195);
  lc.setRow(2, 5, 224);
  lc.setRow(2, 6, 240);
  lc.setRow(2, 7, 240);
  lc.setRow(5, 0, 15);
  lc.setRow(5, 1, 15);
  lc.setRow(5, 2, 15);
  lc.setRow(5, 3, 7);
  lc.setRow(4, 0, 195);
  lc.setRow(4, 1, 195);
  lc.setRow(4, 2, 195);
  lc.setRow(4, 3, 129);
  lc.setRow(3, 0, 240);
  lc.setRow(3, 1, 240);
  lc.setRow(3, 2, 240);
  lc.setRow(3, 3, 224);
  lc.setRow(6, 0, 195);
  lc.setRow(6, 1, 102);
  lc.setRow(6, 2, 60);
  delay(50);
}

//Eyes shut happy mouth closed
void happy1() {
  lc.setRow(0, 7, 3);
  lc.setRow(2, 7, 192);
  lc.setRow(5, 0, 7);
  lc.setRow(5, 1, 12);
  lc.setRow(4, 0, 129);
  lc.setRow(4, 1, 195);
  lc.setRow(3, 0, 224);
  lc.setRow(3, 1, 48);
  lc.setRow(6, 0, 195);
  lc.setRow(6, 1, 102);
  lc.setRow(6, 2, 60);
  delay(50);
}

//Eyes Shut happy mouth open
void happy2() {
  lc.setRow(0, 7, 3);
  lc.setRow(2, 7, 192);
  lc.setRow(5, 0, 7);
  lc.setRow(5, 1, 12);
  lc.setRow(4, 0, 129);
  lc.setRow(4, 1, 195);
  lc.setRow(3, 0, 224);
  lc.setRow(3, 1, 48);
  lc.setRow(6, 0, 255);
  lc.setRow(6, 1, 126);
  lc.setRow(6, 2, 60);
  delay(50);
}

//Eyes Shut happy surprised mouth
void happy3() {
  lc.setRow(0, 7, 3);
  lc.setRow(2, 7, 192);
  lc.setRow(5, 0, 7);
  lc.setRow(5, 1, 12);
  lc.setRow(4, 0, 129);
  lc.setRow(4, 1, 195);
  lc.setRow(3, 0, 224);
  lc.setRow(3, 1, 48);
  lc.setRow(6, 0, 60);
  lc.setRow(6, 1, 102);
  lc.setRow(6, 2, 66);
  lc.setRow(6, 3, 66);
  lc.setRow(6, 4, 102);
  lc.setRow(6, 5, 60);
  delay(50);
}

//Eyes open sad closed mouth
void sad1() {
  lc.setRow(0, 5, 7);
  lc.setRow(0, 6, 15);
  lc.setRow(0, 7, 15);
  lc.setRow(1, 5, 129);
  lc.setRow(1, 6, 195);
  lc.setRow(1, 7, 195);
  lc.setRow(2, 5, 224);
  lc.setRow(2, 6, 240);
  lc.setRow(2, 7, 240);
  lc.setRow(5, 0, 15);
  lc.setRow(5, 1, 15);
  lc.setRow(5, 2, 15);
  lc.setRow(5, 3, 7);
  lc.setRow(4, 0, 195);
  lc.setRow(4, 1, 195);
  lc.setRow(4, 2, 195);
  lc.setRow(4, 3, 125);
  lc.setRow(3, 0, 240);
  lc.setRow(3, 1, 240);
  lc.setRow(3, 2, 240);
  lc.setRow(3, 3, 224);
  lc.setRow(6, 0, 60);
  lc.setRow(6, 1, 102);
  lc.setRow(6, 2, 195);
  delay(50);
}

//Eyes closed sad closed mouth
void sad2() {
  lc.setRow(0, 7, 12);
  lc.setRow(1, 7, 195);
  lc.setRow(2, 7, 48);
  lc.setRow(5, 0, 7);
  lc.setRow(5, 1, 3);
  lc.setRow(4, 0, 129);
  lc.setRow(3, 0, 224);
  lc.setRow(3, 1, 192);
  lc.setRow(6, 0, 60);
  lc.setRow(6, 1, 102);
  lc.setRow(6, 2, 195);
  delay(50);
}

//Eyes closed sad open mouth
void sad3() {
  lc.setRow(0, 7, 12);
  lc.setRow(1, 7, 195);
  lc.setRow(2, 7, 48);
  lc.setRow(5, 0, 7);
  lc.setRow(5, 1, 3);
  lc.setRow(4, 0, 129);
  lc.setRow(3, 0, 224);
  lc.setRow(3, 1, 192);
  lc.setRow(6, 0, 60);
  lc.setRow(6, 1, 126);
  lc.setRow(6, 2, 255);
  delay(50);
}

//Surprised
void surp() {
  lc.setRow(0, 5, 7);
  lc.setRow(0, 6, 15);
  lc.setRow(0, 7, 15);
  lc.setRow(1, 5, 129);
  lc.setRow(1, 6, 195);
  lc.setRow(1, 7, 195);
  lc.setRow(2, 5, 224);
  lc.setRow(2, 6, 240);
  lc.setRow(2, 7, 240);
  lc.setRow(5, 0, 15);
  lc.setRow(5, 1, 15);
  lc.setRow(5, 2, 15);
  lc.setRow(5, 3, 7);
  lc.setRow(4, 0, 195);
  lc.setRow(4, 1, 195);
  lc.setRow(4, 2, 195);
  lc.setRow(4, 3, 125);
  lc.setRow(3, 0, 240);
  lc.setRow(3, 1, 240);
  lc.setRow(3, 2, 240);
  lc.setRow(3, 3, 224);
  lc.setRow(6, 0, 60);
  lc.setRow(6, 1, 102);
  lc.setRow(6, 2, 66);
  lc.setRow(6, 3, 66);
  lc.setRow(6, 4, 102);
  lc.setRow(6, 5, 60);
  delay(50);
}

//Blink
void _blink() {
  lc.setRow(0, 7, 15);
  lc.setRow(1, 7, 195);
  lc.setRow(2, 7, 240);
  lc.setRow(5, 0, 15);
  lc.setRow(5, 1, 15);
  lc.setRow(4, 0, 195);
  lc.setRow(4, 1, 195);
  lc.setRow(3, 0, 240);
  lc.setRow(3, 1, 240);
  lc.setRow(6, 0, 195);
  lc.setRow(6, 1, 102);
  lc.setRow(6, 2, 60);
  delay(50);
}
