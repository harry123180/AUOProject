#include "EdgeComputing.h"
Func F;
#define Size 5
float arr1[Size] = {1.0,2.0,3.0,4.0,5.0};
float arr2[Size] = {5.0,4.0,3.0,2.0,1.0};
float arr3[Size];
float arr_2d[2][Size]= {{5.0,4.0,3.0,2.0,1.0},{5.0,4.0,3.0,2.0,1.0}};
float new_2d[2][Size];
void setup() {
  // put your setup code here, to run once:
Serial.begin(115200);

}

void loop() {
  // put your main code here, to run repeatedly:
//Serial.println(F.F1(1,2));
//F.F2(arr1,arr2,Size,arr3);
/*
for(int i =0;i<Size;i++){
  Serial.println(arr3[i]);
}
*/
F.F3(arr_2d,Size,new_2d);
for(int i =0;i<2;i++){
  for(int j =0;j<Size;j++){
  Serial.println(new_2d[i][j]);
}
}
delay(1000);
}
