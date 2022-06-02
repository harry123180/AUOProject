#include <Wire.h>
#include "FFT.h"
#include <math.h>
//****FFT 必須的變數****//
int Sampling_Rate =5500;
short int TimerRef = 1000000/Sampling_Rate;
#define FFT_N 1024 // Must be a power of 2
const float TOTAL_TIME = FFT_N/Sampling_Rate; // This is equal to FFT_N/sampling_freq
float fft_input0[FFT_N];
float fft_output0[FFT_N];
float fft_input1[FFT_N];
float fft_output1[FFT_N];
float fft_input2[FFT_N];
float fft_output2[FFT_N];
float max_magnitude = 0;
float fundamental_freq = 0;
int fft_signal_X[FFT_N];
int fft_signal_Y[FFT_N];
int fft_signal_Z[FFT_N];
char print_buf[500];
bool flag0 =false;
bool flag1 =false;
bool flag2 =false;

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
double Total_Power(double* Freq_Array){

  /* 頻譜強度總和
   */
  double TP=0;
  for(int i=0;i<FFT_N;i++){
    TP=TP+Freq_Array[i]/1000;
  }
  return TP;
}
double ROP(double* Freq_Array,int F1,int F2){
  /*
   * 頻譜強度比例
   */
   double Power=0;
   for(int i=F1;i<=F2;i++){
    Power = Power+Freq_Array[i]/10;
   }
   return Power/Total_Power(Freq_Array);
}
float Mean(int* Time_Array){
  int time_total=0;
  for(int i =0;i<FFT_N;i++){
    time_total = time_total+Time_Array[i];
  }
  return time_total/FFT_N;
}
float Std(int* Time_Array){
  float avg = Mean(Time_Array);
  float num_Std=0;
  for(int i=0;i<FFT_N;i++){
    num_Std = num_Std + pow(Time_Array[i]-avg,2);
  }
  return num_Std/FFT_N;
}
float RMS(int* Time_Array){
  float MeanSqure=0;
  for(int i=0;i<FFT_N;i++){
    MeanSqure = MeanSqure+ pow(Time_Array[i],2);
  }
  return sqrt(MeanSqure/FFT_N);
}
float Kurtosis(int* Time_Array){
  float avg_Kur = Mean(Time_Array);
  float std_Kur_pow4 = pow(Std(Time_Array),4)*FFT_N;
  float num_Kur =0;
  for(int i=0;i<FFT_N;i++){
    num_Kur = num_Kur+pow(Time_Array[i]-avg_Kur,4);
  }
  return num_Kur/std_Kur_pow4;
}
float Entropy(int* Time_Array){
     float entropy=0;
     float count;
    
      return entropy;
}

 //*******Task任務內容*********//
void taskOne( void * parameter ){
  /*taskone做i2c 讀取adxl的數值 
   * 並將數值存入fft_signal
   * 袴
   */
  while(1){
        //float ROP_v = 
        //float Total_Power_v = 
        float Mean_X = Mean(fft_signal_X);
        float Mean_Y = Mean(fft_signal_Y);
        float Mean_Z = Mean(fft_signal_Z);
        //float Std_v = 
        //float Rms_v = 
        //float Kurtosis_v = 
        sprintf(print_buf,"X : %f \t Y: %f \tZ : %f \t\n", Mean_X, Mean_Y ,Mean_Z);
        Serial.println(print_buf);
        fft_config_t *real_fft_plan_0 = fft_init(FFT_N, FFT_REAL, FFT_FORWARD, fft_input0, fft_output0);
        fft_config_t *real_fft_plan_1 = fft_init(FFT_N, FFT_REAL, FFT_FORWARD, fft_input1, fft_output1);
        fft_config_t *real_fft_plan_2 = fft_init(FFT_N, FFT_REAL, FFT_FORWARD, fft_input2, fft_output2);
        //Serial.println(flag);
        if(flag0 && flag1 && flag2){
          //delay(10);
          //Serial.println("Do FFT");
          flag0 = false;
          flag1 = false;
          flag2 = false;
          for (int k = 0 ; k < FFT_N ; k++){
            real_fft_plan_0->input[k] = (float)fft_signal_X[k];//將fft_signal填入輸入槽位
            real_fft_plan_1->input[k] = (float)fft_signal_Y[k];//將fft_signal填入輸入槽位
            real_fft_plan_2->input[k] = (float)fft_signal_Z[k];//將fft_signal填入輸入槽位  
          }
          fft_execute(real_fft_plan_0);
          fft_execute(real_fft_plan_1);
          fft_execute(real_fft_plan_2);
          for (int k = 1 ; k < real_fft_plan_1->size / 2 ; k++){
            //The real part of a magnitude at a frequency is followed by the corresponding imaginary part in the output
            float mag_0 = sqrt(pow(real_fft_plan_0->output[2*k],2) + pow(real_fft_plan_0->output[2*k+1],2))/1;
            float mag_1 = sqrt(pow(real_fft_plan_1->output[2*k],2) + pow(real_fft_plan_1->output[2*k+1],2))/1;
            float mag_2 = sqrt(pow(real_fft_plan_2->output[2*k],2) + pow(real_fft_plan_2->output[2*k+1],2))/1;
            float freq = k*1.0/TOTAL_TIME;
            //sprintf(print_buf,"%.1f %.1f %.1f",mag_0,mag_1,mag_2);
            //Serial.println(print_buf);
            //sprintf(print_buf,"%.1f ",freq);
            //Serial.println(print_buf);
            if(mag_1 > max_magnitude){
                max_magnitude = mag_1;
                fundamental_freq = freq;
            }     
          }
          
          //sprintf(print_buf,"Fundamental Freq : %f Hz\t Mag: %f g\n", fundamental_freq, (max_magnitude/10000)*2/FFT_N);
          //Serial.println(print_buf);
          flag0 = false;//將fft_sginal填充完畢 flag復位
          flag1 = false;
          flag2 = false;     
        }
        fft_destroy(real_fft_plan_0);//釋放fft記憶體
        fft_destroy(real_fft_plan_1);
        fft_destroy(real_fft_plan_2);
  }
  Serial.println("Ending task 1");
  vTaskDelete( NULL );
}
void IRAM_ATTR onTimer_0() {
  //portEXIT_CRITICAL_ISR(&timerMux_0);
  t0Counter++;
  
  fft_signal_X[t0Counter] = analogRead(FXLN8371Q_X);
  if(t0Counter>FFT_N){
    t0Counter=0;
    //Serial.println("Reset  T0 Sampling Flag");
    flag0 = true; //把flag打開 通知fft可以進行了
  }
  //portEXIT_CRITICAL_ISR(&timerMux_0);
}
void IRAM_ATTR onTimer_1() {
  //portEXIT_CRITICAL_ISR(&timerMux_1);
  t1Counter++;
  //Serial.println("DO onTimer_1");
  fft_signal_Y[t1Counter] = analogRead(FXLN8371Q_Y);
  if(t1Counter>FFT_N){
    //Serial.println("Reset T1 Sampling Flag");
    t1Counter=0;
    flag1 = true; //把flag打開 通知fft可以進行了
  }
  //portEXIT_CRITICAL_ISR(&timerMux_1);
}
void IRAM_ATTR onTimer_2() {
  //portEXIT_CRITICAL_ISR(&timerMux_2);
  t2Counter++;
  fft_signal_Z[t2Counter] = analogRead(FXLN8371Q_Z);
  if(t2Counter>FFT_N){
    t2Counter=0;
    flag2 = true; //把flag打開 通知fft可以進行了
  }
  //portEXIT_CRITICAL_ISR(&timerMux_2);
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
