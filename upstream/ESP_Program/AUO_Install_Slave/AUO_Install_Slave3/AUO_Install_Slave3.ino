
#include <esp_now.h>
#include <WiFi.h>
#include <Wire.h>
#include "FFT.h"
#include <math.h>
// Serial Send Variable

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

//****計時中斷的變數****//
int t0Counter=0;

hw_timer_t * timer_0 = NULL;//宣告一個指向硬體計時器的變量

portMUX_TYPE timerMux_0 = portMUX_INITIALIZER_UNLOCKED;//使用它來處理主循環與ISR之間的同步
void IRAM_ATTR onTimer_0() {
  //portEXIT_CRITICAL_ISR(&timerMux_0);
  ORG_signal[t0Counter] = analogRead(FXLN8371Q_X);
  t0Counter++;
  if(t0Counter>FFT_N){
    t0Counter=0;
    flag0 = true; //把flag打開 通知fft可以進行了
  }
}
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
//*******Task任務內容*********//
void taskOne( void * parameter ){
  while(1){
    Serial.println(flag0);
        if(flag0){
          EC.Convert(ORG_signal,Time_Array);
          data_pkg.Mean_[0] = EC.Mean(Time_Array);
          data_pkg.Std_[0] = EC.Std(Time_Array,data_pkg.Mean_[0]);          
          data_pkg.RMS_[0] = EC.RMS(Time_Array);          
          data_pkg.Kurtosis_[0] = EC.Kurtosis(Time_Array,data_pkg.Mean_[0],data_pkg.Std_[0]);
          flag0 = false;
          fft_config_t *real_fft_plan_0 = fft_init(FFT_N, FFT_REAL, FFT_FORWARD, fft_input0, fft_output0);
          for (int k = 0 ; k < FFT_N ; k++){
            real_fft_plan_0->input[k] = (float)Time_Array[k];//將fft_signal填入輸入槽位
          }
          fft_execute(real_fft_plan_0);
          for (int k = 1 ; k < real_fft_plan_0->size / 2 ; k++){
            //The real part of a magnitude at a frequency is followed by the corresponding imaginary part in the output
            freq_mag[k] = sqrt(pow(real_fft_plan_0->output[2*k],2) + pow(real_fft_plan_0->output[2*k+1],2))/1;        
            float freq = k*1.0/TOTAL_TIME;     
            if(freq_mag[k] >  data_pkg.max_magnitude[0]){
                data_pkg.max_magnitude[0] = freq_mag[k];
                data_pkg.fundamental_freq[0] = freq;
            } 
          }                    
          flag0 = false;//將fft_sginal填充完畢 flag復位                
          fft_destroy(real_fft_plan_0);//釋放fft記憶體  
          data_pkg.tp_[0] = EC.Total_Power(freq_mag); 
          EC_State = true;
          esp_err_t result = esp_now_send(0, (uint8_t *) &data_pkg, sizeof(data_pkg));
          if (result == ESP_OK) {Serial.println("Sent with success");}
          else {Serial.println("Error sending the data");}
        }
  }
  vTaskDelete( NULL );
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
  delay(1000);
  //******計時中斷設定******//
  //為了達到指定sampling rate//
  timer_0 = timerBegin(0, 80, true);
  timerAttachInterrupt(timer_0, &onTimer_0, true);
  timerAlarmWrite(timer_0, TimerRef, true);
  timerAlarmEnable(timer_0);
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
  delay(1000);
}

//                    開發By蘇泓舉
//                    2022.6.30 Final Version
//                       _oo0oo_
//                      o8888888o
//                      88" . "88
//                      (| -_- |)
//                      0\  =  /0
//                    ___/`---'\___
//                  .' \\|     |// '.
//                 / \\|||  :  |||// \
//                / _||||| -:- |||||- \
//               |   | \\\  -  /// |   |
//               | \_|  ''\---/''  |_/ |
//               \  .-\__  '-'  ___/-. /
//             ___'. .'  /--.--\  `. .'___
//          ."" '<  `.___\_<|>_/___.' >' "".
//         | | :  `- \`.;`\ _ /`;.`/ - ` : | |
//         \  \ `_.   \_ __\ /__ _/   .-` /  /
//     =====`-.____`.___ \_____/___.-`___.-'=====
//                       `=---='
//
//
//     ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
//
//               佛祖保佑         永無BUG
//
//
//
