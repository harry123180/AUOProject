#include "EdgeComputing.h"
#include "Arduino.h"
float Func::F1(float v1,float v2){
  return v1+v2;
}
float* Func::F2(float* arr1,float* arr2,int Size,float* arr3){
  for(int i=0;i<=Size;i++){
    arr3[i]=arr1[i]+arr2[i];
  }
  return arr3;
}
Computer::Computer(short int FFT_N,short int Quantity_of_Axis,short int value_of_sensitivity ):m_FFT_N(FFT_N),axis_num(Quantity_of_Axis),sensitivity(value_of_sensitivity){}


void Computer::Convert(int* num_data,float* Time_Array){
  for(int i=0;i<m_FFT_N;i++){
    Time_Array[i] = (num_data[i]-bias)*0.0149;
  }
}
void Computer::Convert_2d(int num_data_2d[][1024],float Time_Array[][1024]){
  
  for(int i=0;i<axis_num;i++){
    for(int j=0;j<m_FFT_N;j++){
      Time_Array[i][j]=(num_data_2d[i][j]-bias)*0.0149;
      
    }
   
  }
}
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
void Computer::Mean_2D(float Time_Array[][1024],double* mean_2d){
  float time_total[axis_num]={0};//初始化全零陣列
  for(int i=0;i<axis_num;i++){
    for(int j =0;j<m_FFT_N;j++){
      time_total[i] = time_total[i]+Time_Array[i][j];  
      }     
    mean_2d[i] = time_total[i]/m_FFT_N;
  }
  //Serial.println(mean_2d[2]);
}
void Computer::Std_2D(float Time_Array[][1024],double* avg,double* std_2d){
  float num_Std[axis_num]={0};
  for(int i=0;i<axis_num;i++){
    for(int j=0;j<m_FFT_N;j++){
      num_Std[i] = num_Std[i] + pow(Time_Array[i][j]-avg[i],2);
    }
    std_2d[i] = num_Std[i]/m_FFT_N;
  }
}
void Computer::RMS_2D(float Time_Array[][1024],double* rms_2d){
  float MeanSqure[axis_num]={0};
  for(int i=0;i<axis_num;i++){
    for(int j=0;j<m_FFT_N;j++){
      MeanSqure[i] = MeanSqure[i]+ pow(Time_Array[i][j],2);
    }
    rms_2d[i]=sqrt(MeanSqure[i]/m_FFT_N);
  }

}
void Computer::Kurtosis_2D(float Time_Array[][1024],double* avg,double* std,double* kurtosis_2d){
  float std_Kur_pow4[axis_num] = {0};
  float num_Kur[axis_num] ={0};
  for(int i=0;i<axis_num;i++){
    std_Kur_pow4[i] = pow(std[i],4)*m_FFT_N;
    for(int j=0;j<m_FFT_N;j++){
      num_Kur[i] = num_Kur[i]+pow(Time_Array[i][j]-avg[i],4);
    }
    kurtosis_2d[i] = num_Kur[i]/std_Kur_pow4[i];
  }
}
void Computer::Total_Power_2D(float Freq_Array[][512],double* total_power_2d){
  float TP[axis_num]={0};
  for(int i=0;i<axis_num;i++){
    for(int j=0;j<m_FFT_N/2;j++){
      //Serial.println(Freq_Array[i][j]);
      total_power_2d[i]=total_power_2d[i]+Freq_Array[i][j];
    }
  }
  
}
void Computer::ROP_2D(float Freq_Array[][512],int* Freq_min,int* Freq_max,double* TP,double* rop_2d){
  float Power[axis_num] = {0};
  for(int i=0;i<=axis_num;i++){
    for(int j=Freq_min[i];j<=Freq_max[i];j++){
      Power[i] = Power[i]+Freq_Array[i][j];
    }
    rop_2d[i]=Power[i]/TP[i];
  }
}
