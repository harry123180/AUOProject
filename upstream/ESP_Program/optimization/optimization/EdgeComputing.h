#ifndef _EDGECOMPUTING_H_
#endif _EDGECOMPUTING_H_
#include <stdlib.h>
#include <stdio.h>
class Func{
  public:
  float F1(float v1,float v2);
  float* F2(float* arr1,float* arr2,int Size,float* arr3);
};
class Computer{
  /*初始化Computer物件 在使用前須宣告
  *其內容如下
  *API Document 有詳細說明每個Function的用法及意義
  *[網址]
  */
  private: 
    short int m_FFT_N;
    short int axis_num;
  public:
    //TIme Domain Index 時域指標
    float Mean(float* Time_Array);//平均數
    float Std(float* Time_Array,float avg);//標準差
    float RMS(float Time_Array);//方均根植
    float Kurtosis(float Time_Array,float avg,float std);//峰度
    //Frequency Domain Index 頻域指標
    float Total_Power(float* Freq_Array);//總功率
    float ROP(float* Freq_Array,int Freq_min,int Freq_max,float TP);//頻譜強度比例
    /* 二維情況 同時計算多軸數據*/
    //TIme Domain Index 時域指標
    float Mean_2D(float** Time_Array,float* mean_2d);//平均數
    float Std_2D(float** Time_Array,float* avg,float* std_2d);//標準差
    float RMS_2D(float** Time_Array,float* rms_2d);//方均根植
    float Kurtosis_2D(float** Time_Array,float* avg,float* std,float* kurtosis_2d);//峰度
    //Frequency Domain Index 頻域指標
    float Total_Power_2D(float** Freq_Array,float* total_power_2d);//總功率
    float ROP_2D(float** Freq_Array,int* Freq_min,int* Freq_max,float* TP,float* rop_2d);//頻譜強度比例
}
