#include <Wire.h>
#include <PubSubClient.h>
#include "FFT.h"
#include <math.h>
// Serial Send Variable
double Mean_[3] = {0};
double Std_[3] = {0};
double RMS_[3] = {0};
double Kurtosis_[3] = {0};
double tp_[3] = {0};
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

char print_buf[500];
bool flag0 =false;
bool flag1 =false;
bool flag2 =false;
bool EC_State=false;
const float num2g = 0.01491970486;
//***FXLN變數****//
const short int FXLN8371Q_X = 36;
const short int FXLN8371Q_Y = 39;
const short int FXLN8371Q_Z = 34;
//****計時中斷的變數****//
int t0Counter=0;
int t1Counter=0;
int t2Counter=0;
hw_timer_t * timer_0 = NULL;//宣告一個指向硬體計時器的變量
hw_timer_t * timer_1 = NULL;
hw_timer_t * timer_2 = NULL;
portMUX_TYPE timerMux_0 = portMUX_INITIALIZER_UNLOCKED;//使用它來處理主循環與ISR之間的同步
portMUX_TYPE timerMux_1 = portMUX_INITIALIZER_UNLOCKED;
portMUX_TYPE timerMux_2 = portMUX_INITIALIZER_UNLOCKED;


 //*******Task任務內容*********//
void taskOne( void * parameter ){
  /*
   * 並將數值存入fft_signal
   * 袴
   */
  while(1){
        sprintf(print_buf,"%d %d %d",flag0,flag1,flag2);
        if(flag0 && flag1 && flag2){
          float max_magnitude[axis_num] = {0};
          float fundamental_freq[axis_num] = {0};
          EC.Convert_2d(ORG_signal,Time_Array);
          EC.Mean_2D(Time_Array,Mean_);
          EC.Std_2D(Time_Array,Mean_,Std_);          
          EC.RMS_2D(Time_Array,RMS_);          
          EC.Kurtosis_2D(Time_Array,Mean_,Std_,Kurtosis_);
          flag0 = false;
          flag1 = false;
          flag2 = false;
          EC_State = true;
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
            
            if(freq_mag[0][k] > max_magnitude[0]){
                max_magnitude[0] = freq_mag[0][k];
                fundamental_freq[0] = freq;
            }
            if(freq_mag[1][k] > max_magnitude[1]){
                max_magnitude[1] = freq_mag[1][k];
                fundamental_freq[1] = freq;
            }   
            if(freq_mag[2][k] > max_magnitude[2]){
                max_magnitude[2] = freq_mag[2][k];
                fundamental_freq[2] =freq;
            }        
          }                    
          flag0 = false;//將fft_sginal填充完畢 flag復位
          flag1 = false;
          flag2 = false;          
          fft_destroy(real_fft_plan_0);//釋放fft記憶體
          fft_destroy(real_fft_plan_1);
          fft_destroy(real_fft_plan_2);   
          EC.Total_Power_2D(freq_mag,tp_); 
          //sprintf(print_buf,"%d %.2f %.2f %.2f %.2f %.2f %.2f %.2f %.2f %.2f %.1f %.1f %.1f %.1f %.1f %.1f %.1f %.1f %.1f\n",1,Mean_[0],Mean_[1],Mean_[2],Std_[0],Std_[1],Std_[2],RMS_[0],RMS_[1],RMS_[2],Kurtosis_[0],Kurtosis_[1],Kurtosis_[2],fundamental_freq[0],fundamental_freq[1],fundamental_freq[2],tp_[0],tp_[1],tp_[2]);
          //sprintf(print_buf,"%.1f %.1f %.1f\n",Mean_[0],Mean_[1],Mean_[2]);
          //Serial.print(print_buf);
          //for(int i =0 ;i<1024;i++){
            //Serial.println(Time_Array[2][i]);
          //}
        }
       
  }
  Serial.println("Ending task 1");
  vTaskDelete( NULL );
}
void taskTwo( void * parameter ){
  while(true){
    //Serial.println(EC_State);
    if(EC_State==true){
      EC_State = false;
      }
  }
}
void IRAM_ATTR onTimer_0() {
  //portEXIT_CRITICAL_ISR(&timerMux_0);
  ORG_signal[0][t0Counter] = analogRead(FXLN8371Q_X);
  t0Counter++;
  
  if(t0Counter>FFT_N){
    t0Counter=0;
    flag0 = true; //把flag打開 通知fft可以進行了
  }
}
void IRAM_ATTR onTimer_1() {
  ORG_signal[1][t1Counter] = analogRead(FXLN8371Q_Y);
  t1Counter++;
  if(t1Counter>FFT_N){
    t1Counter=0;
    flag1 = true; //把flag打開 通知fft可以進行了
  }
}
void IRAM_ATTR onTimer_2() {
  ORG_signal[2][t2Counter] = analogRead(FXLN8371Q_Z);
  t2Counter++;
  if(t2Counter>FFT_N){
    t2Counter=0;
    flag2 = true; //把flag打開 通知fft可以進行了
  }
}

void setup() {
  Serial.begin(115200);
  delay(1000);
  //******計時中斷設定******//
  //為了達到指定sampling rate//
  timer_0 = timerBegin(0, 80, true);
  timerAttachInterrupt(timer_0, &onTimer_0, true);
  timerAlarmWrite(timer_0, TimerRef, true);
  timerAlarmEnable(timer_0);
  
  timer_1 = timerBegin(1, 80, true);
  timerAttachInterrupt(timer_1, &onTimer_1, true);
  timerAlarmWrite(timer_1, TimerRef, true);
  timerAlarmEnable(timer_1);
  
  timer_2 = timerBegin(2, 80, true);
  timerAttachInterrupt(timer_2, &onTimer_2, true);
  timerAlarmWrite(timer_2, TimerRef, true);
  timerAlarmEnable(timer_2);
  
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
  /*
  xTaskCreatePinnedToCore(
    taskTwo, //本任務實際對應的Function
    "TaskTwo", //任務名稱（自行設定）
    10000, //所需堆疊空間（常用10000）
    NULL, //輸入值
    0, //優先序：0為最低，數字越高代表越優先
    NULL, //對應的任務handle變數
    0); //指定執行核心編號（0、1或tskNO_AFFINITY：系統指定）
    

  xTaskCreate(
              taskOne,          ///*任务函数
              "TaskOne",       带任务名称的字符串
              10000,            堆栈大小，单位为字节
              NULL,             作为任务输入传递的参数
              1,                任务的优先级
              NULL);            任务句柄
  xTaskCreate(
              taskTwo,          /* Task function. 
              "TaskTwo",        /* String with name of task. 
              10000,            /* Stack size in bytes. 
              NULL,             /* Parameter passed as input of the task 
              1,                /* Priority of the task. 
              NULL);            /* Task handle. */

}
 
void loop(){
  delay(1);
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
