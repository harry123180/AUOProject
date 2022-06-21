# EdgeComputing.h Libary API Document 
## 以下對於本專案使用之指標數學公式進行說明
### ESP對類比式加速規採樣
> ESP的ADC是SARADC具有12bit的解析度(**resolution**)  
> 加速規輸出一電壓訊號時，經由Analog/Digital轉換之後其轉換公式如下  
> $$acceleration = \frac{workvolt}{resolution}*(Numerical-bias)\div sensitivity$$
### 時域方面
* **平均值**原始數據之平均數值。
>$$\operatorname{Mean}=\frac{1}{n} \sum_{i=1}^{n} x_{i}$$
* **方均根**:原始數據之方均根值，評估訊號振幅。


>$$\mathrm{RMS}=\sqrt{\frac{1}{n} \sum_{i=1}^{n} x_{i}^{2}}$$

* **峰度**:第四中央慣性矩，評估時域訊號中高頻訊號的比例。
>$$ \text { Kurtosis }=\frac{1}{n} \frac{\sum_{i=1}^{n}\left(x_{i}-\mu\right)^{4}}{\sigma^{4}} $$

* **標準差**原始數據之標準差，代表扣除平均值的訊號振幅。
>$$\text { std }=\sqrt{\frac{\sum_{i=1}^{n}\left(x_{i}-\mu\right)^{2}}{n-1}} $$
### 頻域方面
* **頻譜強度總和**:透過在有興趣頻段對PSD做積分即可獲得總功率。
>$$ \text { Total power }=\int_{0}^{f_{s} / 2} S(f) d f $$
* **頻譜強度比例(Ratio of power,ROP)**:此方法主要應用頻寬較大之感測器，頻域訊號依照頻率分段，並以頻段內的總頻譜強度除以頻譜強度總和即為該頻段之頻譜強度比例。
>$$ \text { ROP }=\frac{\int_{f_{1}}^{f_{2}} S(f) d f}{\text { Total power }} $$

### 在ESP32 Program 邊緣計算部分過於複雜，因此獨立編寫一個庫，方便管理及說明
* 整個EdgeComputing庫裡面共有兩個物件可以宣告
1. 第一個是```Func```
2. 第二個是```Computer```

以下是使用範本

```
#include "EdgeComputing.h"
Computer 物件名;
物件名.API();
```
###```Func```為測試用物件，單純實現加法庫。

### ```Computer```為管理指標運算的物件，裡面API說明如下:
> ```float Mean(float* Time_Array);```
> * 輸入參數: 
>>```Time_Array```:時域數據陣列
> * 回傳:
>>```Mean```:平均數

> ```float Std(float* Time_Array,float avg);```
> * 輸入參數: 
>>```Time_Array``` :時域數據陣列  
>>```avg```: 時域數據陣列之平均值
> * 回傳:
>> ```std```:時域數據陣列之標準差

> ```float RMS(float Time_Array);```
> * 輸入參數:
>>```Time_Array```:時域數據陣列
> * 回傳:
>> ```rms```:時域數據陣列之方均根值

> ``` float Kurtosis(float Time_Array,float avg,float std);```
> * 輸入參數:
>> ```Time_Array```:時域數據陣列  
>> ```avg```: 時域數據陣列之平均值  
>> ```std```: 時域數據陣列之標準差
> * 回傳:
>> ```kurtosis```: 時域數據陣列之峰度指標

> ```float Total_Power(float* Freq_Array);```
> * 輸入參數:
>> ```Freq_Array```:經過FFT之後的頻域數據陣列
> * 回傳:
>> ```TP```: 整個頻譜的功率和

> ```float ROP(float* Freq_Array,int Freq_min,int Freq_max,float TP);```
> * 輸入參數:
>> ```Freq_Array```:經過FFT之後的頻域數據陣列
>> ```Freq_min```:有興趣頻段的最小
>> ```Freq_max```:有興趣頻段的最大
> * 回傳:
>> ```rop```: 頻譜強度比例

> ```float Mean_2D(float** Time_Array,float* mean_2d);```
> * 輸入參數:
>> ```Time_Array```:二維時域數據[軸][採樣buffer長度]  
>> ```mean_2d```:空的一維陣列，用以存放各軸計算結果，長度為軸數
> * 回傳:
>> ```mean_2d```:計算好的各軸計算結果

> ```float Std_2D(float** Time_Array,float* avg,float* std_2d);```
> * 輸入參數:
>> ```Time_Array```:二維時域數據[軸][採樣buffer長度]  
>> ```avg```:一維陣列，存放各軸平均值  
>> ```std_2d```:空的一維陣列，用以存放各軸計算結果，長度為軸數
> * 回傳:
>> ```std_2d```:計算好的各軸計算std結果

> ```float RMS_2D(float** Time_Array,float* rms_2d);```
> * 輸入參數:
>> ```Time_Array```:二維時域數據[軸][採樣buffer長度]  
>> ```rms_2d```:空的一維陣列，用以存放各軸計算結果，長度為軸數
> * 回傳:
>> ```rms_2d```:計算好的各軸計算rms結果
> ```float Kurtosis_2D(float** Time_Array,float* avg,float* std,float* kurtosis_2d);```
> * 輸入參數:
>> ```Time_Array```:二維時域數據[軸][採樣buffer長度]  
>> ```avg```:一維陣列，存放各軸平均值  
>> ```std```:一維陣列，存放各軸標準差  
>> ```kurtosis_2d```:空的一維陣列，用以存放各軸計算結果，長度為軸數
> * 回傳:
>> ```kurtosis_2d```:計算好的各軸計算kurtosis結果

> ```float Total_Power_2D(float** Freq_Array,float* total_power_2d);```
> * 輸入參數:
>>```Freq_Array```:經過FFT之二維頻域數據[軸][採樣buffer長度]  
>>```total_power_2d```:空的一維陣列，用以存放各軸計算結果，長度為軸數
> * 回傳:
>>```total_power_2d```:計算好的各軸計算TP結果

> ```float ROP_2D(float** Freq_Array,int* Freq_min,int* Freq_max,float* TP,float* rop_2d);```
> * 輸入參數:
>>```Freq_Array```:經過FFT之二維頻域數據[軸][採樣buffer長度]  
>>```Freq_min```:存放各軸有興趣頻段最小值之一維陣列 
>>```Freq_max```:存放各軸有興趣頻段最大值之一維陣列 
>>```rop_2d```:空的一維陣列，用以存放各軸計算結果，長度為軸數
> * 回傳:
>>```rop_2d```:計算好的各軸計算rop結果
