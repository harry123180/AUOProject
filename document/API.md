# EdgeComputing.h Libary API Document 
## 以下對於本專案使用之指標數學公式進行說明
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

```buildoutcfg
#include "EdgeComputing.h"
Computer 物件名;
物件名.API();
```
###```Func```為測試用物件，單純實現加法庫。

### ```Computer```為管理指標運算的物件，裡面API說明如下:
> ```float Mean(float* Time_Array);```
> * 輸入參數: 時域數據陣列