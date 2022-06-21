#include "EdgeComputing.h"
float Func::F1(float v1,float v2){
  return v1+v2;
}
float* Func::F2(float* arr1,float* arr2,int Size,float* arr3){
  for(int i=0;i<=Size;i++){
    arr3[i]=arr1[i]+arr2[i];
  }
  return arr3;
}
void Func::F3(float arr[][Size],int Size,float arr3[][Size]){
  for(int i=0;i<=Size;i++){
    arr3[0][i]=arr[0][i]+arr[1][i];
    arr3[1][i]=arr[0][i]-arr[1][i];
  }
}
Computer::Computer(short int FFT_N,short int Quantity_of_Axis,short int value_of_sensitivity ):m_FFT_N(FFT_N),axis_num(Quantity_of_Axis),sensitivity(value_of_sensitivity){}

float Computer::Mean(float* Time_Array){
  float time_total=0;
  for(int i =0;i<m_FFT_N;i++){
    time_total = time_total+Time_Array[i]; 
  }
  return time_total/m_FFT_N;
}
float Computer::Std(float* Time_Array,float avg){
float num_Std=0;
  for(int i=0;i<m_FFT_N;i++){
    num_Std = num_Std + pow(Time_Array[i]-avg,2);
  }
  return num_Std/m_FFT_N;
}
float Computer::RMS(float* Time_Array){
  float MeanSqure=0;
  for(int i=0;i<m_FFT_N;i++){
    MeanSqure = MeanSqure+ pow(Time_Array[i],2);
  }
  return sqrt(MeanSqure/m_FFT_N);
}
float Computer::Kurtosis(float* Time_Array,float avg,float std){
  float std_Kur_pow4 = pow(std,4)*m_FFT_N;
  float num_Kur =0;
  for(int i=0;i<m_FFT_N;i++){
    num_Kur = num_Kur+pow(Time_Array[i]-avg,4);
  }
  return num_Kur/std_Kur_pow4;
}
float Computer::Total_Power(float* Freq_Array){
  double TP=0;
  for(int i=0;i<m_FFT_N;i++){
    TP=TP+Freq_Array[i];
  }
  return TP;
}
float Computer::ROP(float* Freq_Array,int Freq_min,int Freq_max,float TP){
  double Power=0;
  for(int i=Freq_min;i<=Freq_max;i++){
    Power = Power+Freq_Array[i];
  }
  return Power/TP;
}
/*****************************************************************************/
/* 2D Function 實現*/
float* Computer::Mean_2D(float** Time_Array,float* mean_2d){
  float time_total[axis_num]={0};//初始化全零陣列
  for(int i=0;i<axis_num;i++){
    for(int j =0;j<m_FFT_N;j++){
      time_total[axis_num] = time_total[axis_num]+Time_Array[i][j];  
      }
    mean_2d[i] = time_total[axis_num]/m_FFT_N;
  }
  
  return mean_2d;
}
float* Computer::Std_2D(float** Time_Array,float* avg,float* std_2d){
  float num_Std[axis_num]={0};
  for(int i=0;i<axis_num;i++){
    for(int j=0;j<m_FFT_N;j++){
      num_Std[axis_num] = num_Std[axis_num] + pow(Time_Array[i][j]-avg[i],2);
    }
    std_2d[i] = num_Std[axis_num]/m_FFT_N;
  }
  return std_2d;
}
float* Computer::RMS_2D(float** Time_Array,float* rms_2d){
  float MeanSqure[axis_num]={0};
  for(int i=0;i<axis_num;i++){
    for(int j=0;j<m_FFT_N;j++){
      MeanSqure[axis_num] = MeanSqure[axis_num]+ pow(Time_Array[i][j],2);
    }
    rms_2d[i]=sqrt(MeanSqure[axis_num]/m_FFT_N);
  }
  return rms_2d;
}
float* Computer::Kurtosis_2D(float** Time_Array,float* avg,float* std,float* kurtosis_2d){
  float std_Kur_pow4[axis_num] = {0};
  float num_Kur[axis_num] ={0};
  for(int i=0;i<axis_num;i++){
    std_Kur_pow4[i] = pow(std[i],4)*m_FFT_N;
    for(int j=0;j<m_FFT_N;j++){
      num_Kur[i] = num_Kur[i]+pow(Time_Array[i][j]-avg[i],4);
    }
    kurtosis_2d[i] = num_Kur[i]/std_Kur_pow4[i];
  }
  return kurtosis_2d;
}
float* Computer::Total_Power_2D(float** Freq_Array,float* total_power_2d){
  float TP[axis_num]={0};
  for(int i=0;i<axis_num;i++){
    for(int j=0;j<m_FFT_N;j++){
      total_power_2d[axis_num]=total_power_2d[axis_num]+Freq_Array[i][j];
    }
  }
  return total_power_2d;
}
float* Computer::ROP_2D(float** Freq_Array,int* Freq_min,int* Freq_max,float* TP,float* rop_2d){
  float Power[axis_num] = {0};
  for(int i=0;i<=axis_num;i++){
    for(int j=Freq_min[i];j<=Freq_max[i];j++){
      Power[i] = Power[i]+Freq_Array[i][j];
    }
    rop_2d[i]=Power[i]/TP[i];
  }
  return rop_2d;
}
