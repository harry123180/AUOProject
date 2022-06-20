# EdgeComputing.h Libary API Document 
>* **平均值**原始數據之平均數值。
>$$
>\operatorname{Mean}=\frac{1}{n} \sum_{i=1}^{n} x_{i}
>$$
* **標準差**原始數據之標準差，代表扣除平均值的訊號振幅。
$$
\mathrm{RMS}=\sqrt{\frac{1}{n} \sum_{i=1}^{n} x_{i}^{2}}
$$
* **方均根**:原始數據之方均根值，評估訊號振幅。
$$
\text { Kurtosis }=\frac{1}{n} \frac{\sum_{i=1}^{n}\left(x_{i}-\mu\right)^{4}}{\sigma^{4}}
$$

$$
\text { std }=\sqrt{\frac{\sum_{i=1}^{n}\left(x_{i}-\mu\right)^{2}}{n-1}}
$$

$$
\text { Total power }=\int_{0}^{f_{s} / 2} S(f) d f
$$

$$
\text { ROP }=\frac{\int_{f_{1}}^{f_{2}} S(f) d f}{\text { Total power }}
$$

