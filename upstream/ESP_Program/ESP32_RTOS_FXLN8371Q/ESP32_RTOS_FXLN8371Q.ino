#include <Wire.h>
#include "FFT.h"
//****FFT 必須的變數****//
#define FFT_N 1024 // Must be a power of 2
#define TOTAL_TIME 0.0512 // This is equal to FFT_N/sampling_freq
float fft_input[FFT_N];
float fft_output[FFT_N];
float max_magnitude = 0;
float fundamental_freq = 0;
double fft_signal[FFT_N];
char print_buf[300];
bool flag =false;
//***FXLN變數****//
const short int FXLN8371Q_X = 4;
const short int FXLN8371Q_Y = 2;
const short int FXLN8371Q_Z = 15;
//****計時中斷的變數****//
volatile int interruptCounter;//Main loop 與 ISR 共享之變數 要用volatile聲明 不然會被編譯器優化之後刪除
int totalInterruptCounter;//用以計數發生了幾次中斷
hw_timer_t * timer = NULL;//宣告一個指向硬體計時器的變量
portMUX_TYPE timerMux = portMUX_INITIALIZER_UNLOCKED;//使用它來處理主循環與ISR之間的同步
//*******Task任務內容*********//
void taskOne( void * parameter ){
  /*taskone做i2c 讀取adxl的數值 
   * 並將數值存入fft_signal
   * 
   */
  while(1){
        fft_config_t *real_fft_plan = fft_init(FFT_N, FFT_REAL, FFT_FORWARD, fft_input, fft_output);
        if(flag){
          flag = false;
          for (int k = 0 ; k < FFT_N ; k++)
            real_fft_plan->input[k] = (float)fft_signal[k];//將fft_signal填入輸入槽位  
          fft_execute(real_fft_plan);
          for (int k = 1 ; k < real_fft_plan->size / 2 ; k++){
            //The real part of a magnitude at a frequency is followed by the corresponding imaginary part in the output
            float mag = sqrt(pow(real_fft_plan->output[2*k],2) + pow(real_fft_plan->output[2*k+1],2))/1;
            float freq = k*1.0/TOTAL_TIME;
            //sprintf(print_buf,"%1f", freq);
            //Serial.println(print_buf);
            if(mag > max_magnitude){
                max_magnitude = mag;
                fundamental_freq = freq;
            }     
          }
          //sprintf(print_buf,"Fundamental Freq : %f Hz\t Mag: %f g\n", fundamental_freq, (max_magnitude/10000)*2/FFT_N);
          //Serial.println(print_buf);
          
          flag = false;//將fft_sginal填充完畢 flag復位     
        
        }
        fft_destroy(real_fft_plan);//釋放fft記憶體
  }
  Serial.println("Ending task 1");
  vTaskDelete( NULL );
}
void IRAM_ATTR onTimer() {
  portENTER_CRITICAL_ISR(&timerMux);
  interruptCounter++;
  
  fft_signal[interruptCounter] = analogRead(FXLN8371Q_Z);

  if(interruptCounter>FFT_N){
    interruptCounter=0;
    //Serial.println("Reset Sampling Flag");
    flag = true; //把flag打開 通知fft可以進行了
  }
  portEXIT_CRITICAL_ISR(&timerMux);
}
void setup() {
  Serial.begin(115200);
  delay(1000);
  //******計時中斷設定******//
  //為了達到指定sampling rate//
  timer = timerBegin(0, 80, true);
  timerAttachInterrupt(timer, &onTimer, true);
  timerAlarmWrite(timer, 60, true);
  timerAlarmEnable(timer);
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
