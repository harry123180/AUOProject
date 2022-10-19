//接收器 (執行端)
#include <esp_now.h>
#include <WiFi.h>
#define axis_num 3
//Structure example to receive data
//Must match the sender structure
typedef struct data_package {
int num;  
double Mean_[3];
double Std_[3];
double RMS_[3];
double Kurtosis_[3];
double tp_[3];
float max_magnitude[axis_num];
float fundamental_freq[axis_num];
} data_package;

data_package data_pkg;

char print_buf[500];
//callback function that will be executed when data is received
void OnDataRecv(const uint8_t * mac, const uint8_t *incomingData, int len) {
  memcpy(&data_pkg, incomingData, sizeof(data_pkg));
  /*
  Serial.print("Bytes received: ");
  Serial.println(len);
  Serial.print("Mean_[0] ");
  Serial.println(data_pkg.Mean_[0]);
  Serial.print("Mean_[1] ");
  Serial.println(data_pkg.Mean_[1]);
  Serial.print("Mean_[2] ");
  Serial.println(data_pkg.Mean_[2]);
  Serial.println();
  */
 sprintf(print_buf,"%d %.2f %.2f %.2f %.2f %.2f %.2f %.2f %.2f %.2f %.1f %.1f %.1f %.1f %.1f %.1f %.1f %.1f %.1f\n",
 data_pkg.num,
 data_pkg.Mean_[0],data_pkg.Mean_[1],data_pkg.Mean_[2],
 data_pkg.Std_[0],data_pkg.Std_[1],data_pkg.Std_[2],
 data_pkg.RMS_[0],data_pkg.RMS_[1],data_pkg.RMS_[2],
 data_pkg.Kurtosis_[0],data_pkg.Kurtosis_[1],data_pkg.Kurtosis_[2],
 data_pkg.fundamental_freq[0],data_pkg.fundamental_freq[1],data_pkg.fundamental_freq[2],
 data_pkg.tp_[0],data_pkg.tp_[1],data_pkg.tp_[2]);
 Serial.print(print_buf);
}
 
void setup() {
  //Initialize Serial Monitor
  Serial.begin(115200);
  WiFi.mode(WIFI_STA);
  //Init ESP-NOW
  if (esp_now_init() != ESP_OK) {
    Serial.println("Error initializing ESP-NOW");
    return;
  }
  esp_now_register_recv_cb(OnDataRecv);
}
 
void loop() {

}
