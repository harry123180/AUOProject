#include <Adafruit_ADS1X15.h>
#include <esp_now.h>
#include <WiFi.h>
Adafruit_ADS1115 ads;  /* Use this for the 16-bit version */
//Adafruit_ADS1015 ads;     /* Use this for the 12-bit version */
int left_Relay=12;
int right_Relay=14;
// 放入接收器的MAC地址
uint8_t broadcastAddress1[] = {0x7C, 0x9E, 0xBD, 0x09, 0xE8, 0x00};
typedef struct data_package {
int num=5;
#define axis_num  3//總共有三軸
double Mean_[3] = {0};
double Std_[3] = {0};
double RMS_[3] = {0};
double Kurtosis_[3] = {0};
double tp_[3] = {0};
float max_magnitude[axis_num] = {0};
float fundamental_freq[axis_num] = {0};
} data_package;

data_package data_pkg;
esp_now_peer_info_t peerInfo;
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
void setup(void)
{
  Serial.begin(115200);
  pinMode(left_Relay,OUTPUT);
  pinMode(right_Relay,OUTPUT);
  
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
  
  Serial.println("Hello!");
  Serial.println("Getting differential reading from AIN0 (P) and AIN1 (N)");
  Serial.println("ADC Range: +/- 6.144V (1 bit = 3mV/ADS1015, 0.1875mV/ADS1115)");
  
  if (!ads.begin()) {
    Serial.println("Failed to initialize ADS.");
    while (1);
  }
  
  }

void loop(void)
{
  
  int16_t results;
  float multiplier = 0.1875F; /* ADS1115  @ +/- 6.144V gain (16-bit results) */
  digitalWrite(left_Relay,HIGH);
  digitalWrite(right_Relay,LOW);
  data_pkg.Mean_[0] = ads.readADC_Differential_0_1()* multiplier;
  delay(1000);
  digitalWrite(left_Relay,LOW);
  digitalWrite(right_Relay,HIGH);
  data_pkg.Mean_[1] = ads.readADC_Differential_0_1()* multiplier;
  Serial.print("Left: ");
  Serial.print(data_pkg.Mean_[0]);
  Serial.print("Right: "); 
  Serial.println(data_pkg.Mean_[1]); 
  
  //esp_err_t result = esp_now_send(0, (uint8_t *) &data_pkg, sizeof(data_pkg));  
  delay(1000);
}
