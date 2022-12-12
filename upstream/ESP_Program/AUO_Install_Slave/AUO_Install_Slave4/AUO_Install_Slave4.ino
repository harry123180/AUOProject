#include <esp_now.h>
#include <WiFi.h>
#include <Wire.h>
#include "FFT.h"
#include <math.h>
// Serial Send Variable
#include <Adafruit_ADS1X15.h>

// Adafruit_ADS1115 ads;  /* Use this for the 16-bit version */
Adafruit_ADS1015 ads;     /* Use this for the 12-bit version */
/* EdegComputing宣告*/
#include "EdgeComputing.h"
#define axis_num  1//總共有1軸
short int sensitivity = 41;
#define FFT_N 1024 // Must be a power of 2
Computer EC(FFT_N,axis_num,sensitivity);

//****FFT 必須的變數****//
int Sampling_Rate =5500;
short int TimerRef = 1000000/Sampling_Rate;
const float TOTAL_TIME = 0.1861; // This is equal to FFT_N/sampling_freq
float fft_input0[FFT_N];
float fft_output0[FFT_N];
float freq_mag[FFT_N/2];
int ORG_signal[FFT_N];
float Time_Array[FFT_N];
char print_buf[500];
bool flag0 =false;
bool EC_State=false;
//***FXLN變數****//
const short int FXLN8371Q_X = 36;


// 放入接收器的MAC地址
uint8_t broadcastAddress1[] = {0x7C, 0x9E, 0xBD, 0x09, 0xE8, 0x00};
typedef struct data_package {
int num=3;
double Mean_[3] = {0};
double Std_[3] = {0};
double RMS_[3] = {0};
double Kurtosis_[3] = {0};
double tp_[3] = {0};
float max_magnitude[axis_num] = {0};
float fundamental_freq[axis_num] = {0};
} data_package;
data_package data_pkg;
// 數據發送時回調
void OnDataSent(const uint8_t *mac_addr, esp_now_send_status_t status) {
  char macStr[18];
  // 將發件人mac地址複製到一個字符串
  Serial.println("SEND");
  snprintf(macStr, sizeof(macStr), "%02x:%02x:%02x:%02x:%02x:%02x",
           mac_addr[0], mac_addr[1], mac_addr[2], mac_addr[3], mac_addr[4], mac_addr[5]);
}

void setup() {
  Serial.begin(115200);
    WiFi.mode(WIFI_STA);
  if (esp_now_init() != ESP_OK) {
    Serial.println("Error initializing ESP-NOW");
    return;
  }
  esp_now_register_send_cb(OnDataSent);
  // register peer
  esp_now_peer_info_t peerInfo;
  peerInfo.channel = 0;  
  peerInfo.encrypt = false;
  // register first peer  
  memcpy(peerInfo.peer_addr, broadcastAddress1, 6);
  if (esp_now_add_peer(&peerInfo) != ESP_OK){
    
    Serial.println("Failed to add peer");
    return;
  }
  if (!ads.begin()) {
    Serial.println("Failed to initialize ADS.");
    while (1);
  }
  delay(1000);
  
  
}
 
void loop() {
  int16_t results_v;

  /* Be sure to update this value based on the IC and the gain settings! */
  float   multiplier = 3.0F;    /* ADS1015 @ +/- 6.144V gain (12-bit results) */
  //float multiplier = 0.1875F; /* ADS1115  @ +/- 6.144V gain (16-bit results) */

  results_v = ads.readADC_Differential_0_1();
  data_pkg.Mean_[0] = results_v * multiplier;
  results_v = ads.readADC_Differential_2_3();
  data_pkg.Mean_[1] = results_v * multiplier;
  esp_err_t result = esp_now_send(broadcastAddress1, (uint8_t *) &data_pkg, sizeof(data_pkg));
  
  delay(1000);
}
