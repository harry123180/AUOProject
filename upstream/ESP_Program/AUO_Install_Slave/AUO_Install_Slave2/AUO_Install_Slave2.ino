//MPU6050
#include <esp_now.h>
#include <WiFi.h>
#include <Wire.h>
#include "FFT.h"
#include <math.h>
#include <Wire.h>
const int MPU = 0x68;
int16_t AcX, AcY, AcZ;
float gForceX, gForceY, gForceZ;
float orgdata[3][150];
// Serial Send Variable
// 放入接收器的MAC地址
uint8_t broadcastAddress1[] = {0x7C, 0x9E, 0xBD, 0x09, 0xE8, 0x00};
//0x7C, 0x9E, 0xBD, 0x09, 0xE8, 0x00
//0x58, 0xBF, 0x25, 0x81, 0x69, 0x14
//84:F7:03:7A:FE:06
//0x84, 0xF7, 0x03, 0x7A, 0xFE, 0x06

/* EdegComputing宣告*/
#include "EdgeComputing.h"
#define axis_num  3//總共有三軸
short int sensitivity = 54;
#define FFT_N 1024 // Must be a power of 2
Computer EC(FFT_N,axis_num,sensitivity);

//****FFT 必須的變數****//
int Sampling_Rate =5500;
short int TimerRef = 1000000/Sampling_Rate;
const float TOTAL_TIME = 0.1861; // This is equal to FFT_N/sampling_freq
float fft_input0[FFT_N];
float fft_output0[FFT_N];
float fft_input1[FFT_N];
float fft_output1[FFT_N];
float fft_input2[FFT_N];
float fft_output2[FFT_N];
float freq_mag[axis_num][FFT_N/2];
int ORG_signal[axis_num][FFT_N];
float Time_Array[axis_num][FFT_N];
bool flag0 = false;
char print_buf[500];
bool EC_State=false;
typedef struct data_package {
int num=2;
double Mean_[3] = {0};
double Std_[3] = {0};
double RMS_[3] = {0};
double Kurtosis_[3] = {0};
double tp_[3] = {0};
float max_magnitude[axis_num] = {0};
float fundamental_freq[axis_num] = {0};
} data_package;

data_package data_pkg;
esp_now_peer_info_t peerInfo;//line 185
// 數據發送時回調
void OnDataSent(const uint8_t *mac_addr, esp_now_send_status_t status) {
  char macStr[18];
  Serial.print("Packet to: ");
  // 將發件人mac地址複製到一個字符串
  snprintf(macStr, sizeof(macStr), "%02x:%02x:%02x:%02x:%02x:%02x",
           mac_addr[0], mac_addr[1], mac_addr[2], mac_addr[3], mac_addr[4], mac_addr[5]);
  Serial.print(macStr);
  Serial.print(" send status:\t");
  Serial.println(status == ESP_NOW_SEND_SUCCESS ? "Delivery Success" : "Delivery Fail");
}
//*******Task任務內容*********//
void taskOne( void * parameter ){
  while(1){
        sprintf(print_buf,"%d",flag0);
        if(flag0){
          //EC.Convert_2d(ORG_signal,Time_Array);
          EC.Mean_2D(Time_Array,data_pkg.Mean_);
          EC.Std_2D(Time_Array,data_pkg.Mean_,data_pkg.Std_);          
          EC.RMS_2D(Time_Array,data_pkg.RMS_);          
          EC.Kurtosis_2D(Time_Array,data_pkg.Mean_,data_pkg.Std_,data_pkg.Kurtosis_);
           Serial.print(data_pkg.Kurtosis_[0]);
           Serial.print(" ");
           Serial.print(data_pkg.Kurtosis_[1]);
           Serial.print(" ");
           Serial.println(data_pkg.Kurtosis_[2]);
          fft_config_t *real_fft_plan_0 = fft_init(FFT_N, FFT_REAL, FFT_FORWARD, fft_input0, fft_output0);
          fft_config_t *real_fft_plan_1 = fft_init(FFT_N, FFT_REAL, FFT_FORWARD, fft_input1, fft_output1);
          fft_config_t *real_fft_plan_2 = fft_init(FFT_N, FFT_REAL, FFT_FORWARD, fft_input2, fft_output2);
          for (int k = 0 ; k < FFT_N ; k++){
            real_fft_plan_0->input[k] = (float)Time_Array[0][k];//將fft_signal填入輸入槽位
            real_fft_plan_1->input[k] = (float)Time_Array[1][k];//將fft_signal填入輸入槽位
            real_fft_plan_2->input[k] = (float)Time_Array[2][k];//將fft_signal填入輸入槽位  
          }
          fft_execute(real_fft_plan_0);
          fft_execute(real_fft_plan_1);
          fft_execute(real_fft_plan_2);
          for (int k = 1 ; k < real_fft_plan_1->size / 2 ; k++){
            //The real part of a magnitude at a frequency is followed by the corresponding imaginary part in the output
            freq_mag[0][k] = sqrt(pow(real_fft_plan_0->output[2*k],2) + pow(real_fft_plan_0->output[2*k+1],2))/1;
            freq_mag[1][k] = sqrt(pow(real_fft_plan_1->output[2*k],2) + pow(real_fft_plan_1->output[2*k+1],2))/1;
            freq_mag[2][k] = sqrt(pow(real_fft_plan_2->output[2*k],2) + pow(real_fft_plan_2->output[2*k+1],2))/1;
            float freq = k*1.0/TOTAL_TIME;           
            if(freq_mag[0][k] >  data_pkg.max_magnitude[0]){
                data_pkg.max_magnitude[0] = freq_mag[0][k];
                data_pkg.fundamental_freq[0] = freq;
            }
            if(freq_mag[1][k] >  data_pkg.max_magnitude[1]){
                data_pkg.max_magnitude[1] = freq_mag[1][k];
                data_pkg.fundamental_freq[1] = freq;
            }   
            if(freq_mag[2][k] >  data_pkg.max_magnitude[2]){
                data_pkg.max_magnitude[2] = freq_mag[2][k];
                data_pkg.fundamental_freq[2] =freq;
            }        
          }                    
          fft_destroy(real_fft_plan_0);//釋放fft記憶體
          fft_destroy(real_fft_plan_1);
          fft_destroy(real_fft_plan_2);   
          EC.Total_Power_2D(freq_mag,data_pkg.tp_); 
          EC_State = true; 
          esp_err_t result = esp_now_send(0, (uint8_t *) &data_pkg, sizeof(data_pkg));
          vTaskDelay(3000);
          flag0 = false;//將fft_sginal填充完畢 flag復位
        }
  }
  Serial.println("Ending task 1");
  vTaskDelete( NULL );
}


void dataReceiver(){
  Wire.beginTransmission(MPU);
  Wire.write(0x3B);  // starting with register 0x3B (ACCEL_XOUT_H)
  Wire.endTransmission(false);
  Wire.requestFrom(MPU,6,true);  // request a total of 14 registers
  AcX = Wire.read()<<8|Wire.read();  // 0x3B (ACCEL_XOUT_H) & 0x3C (ACCEL_XOUT_L)     
  AcY = Wire.read()<<8|Wire.read();  // 0x3D (ACCEL_YOUT_H) & 0x3E (ACCEL_YOUT_L)
  AcZ = Wire.read()<<8|Wire.read();  // 0x3F (ACCEL_ZOUT_H) & 0x40 (ACCEL_ZOUT_L)
  processData();
}
void processData(){
  gForceX = AcX / 16384.0;
  gForceY = AcY / 16384.0; 
  gForceZ = AcZ / 16384.0;
}
void debugFunction(int16_t AcX, int16_t AcY, int16_t AcZ,uint8_t i){
  Time_Array[0][i]=gForceX;
  Time_Array[1][i]=gForceY;
  Time_Array[2][i]=gForceZ;
  /*
  Serial.print(gForceX);
  Serial.print(" ");
  Serial.print(gForceY);
  Serial.print(" ");
  Serial.println(gForceZ);*/
}
void setup() {
  Serial.begin(115200);
  Wire.begin(21,22);
  Wire.beginTransmission(MPU);
  Wire.write(0x6B);  // PWR_MGMT_1 register
  Wire.write(0);     // set to zero (wakes up the MPU-6050)
  Wire.endTransmission(true);
  WiFi.mode(WIFI_STA);
  if (esp_now_init() != ESP_OK) {
    Serial.println("Error initializing ESP-NOW");
    return;
  }
  esp_now_register_send_cb(OnDataSent);
  memcpy(peerInfo.peer_addr, broadcastAddress1, 6);
  peerInfo.channel = 0;  
  peerInfo.encrypt = false;
 
  if (esp_now_add_peer(&peerInfo) != ESP_OK){
    
    Serial.println("Failed to add peer");
    return;
  }
  delay(1000);
  //
  //Task宣告及初期設定
  xTaskCreatePinnedToCore(
  taskOne, //本任務實際對應的Function
  "TaskOne", //任務名稱（自行設定）
  10000, //所需堆疊空間（常用10000）
  NULL, //輸入值
  0, //優先序：0為最低，數字越高代表越優先
  NULL, //對應的任務handle變數
  tskNO_AFFINITY); //指定執行核心編號（0、1或tskNO_AFFINITY：系統指定）


}
void loop() {
  for(int i=0;i<FFT_N;i++){
  dataReceiver();
  debugFunction(AcX,AcY,AcZ,i);
  }
  flag0=true;
}
