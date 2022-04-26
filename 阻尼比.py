from matplotlib import pyplot as plt
import  numpy as np
from scipy.fft import fft, fftfreq
file1 = open('test752.txt', 'r')
Lines = file1.readlines()
ch1 =[]
Title = 'damping'
sampling_rate = 1653 #設定採樣頻率
# Strips the newline character
Sensitivity = 1 # 單位mv/g
N = 20480 #考慮的點數 為的冪次
start_time = 2.53 #開始晃動的時間 單位sec
for line in Lines:
    a = line.strip()
    ch1.append(float(a.split()[1])*Sensitivity)
t=  np.linspace(0, int(len(ch1)/sampling_rate),int(len(ch1)))
plt.ion()
#y_f = np.abs(np.fft.fft(y_data_OUT))
fig = plt.figure(figsize=(8,10))
ax1 = fig.add_subplot(211)#2個圖 橫版只放1 1號位置
ax2 = fig.add_subplot(212)#2個圖 橫版只放1 2號位置
#ax3 = fig.add_subplot(212)#2個圖 橫版只放1 2號位置
ax1.plot(t,ch1)
ax1.set_title(Title)
ax1.set(xlabel='Time(Sec)', ylabel='Acceleration(g)')
fft_y = fft(ch1[int(start_time*sampling_rate):len(ch1)])
abs_y=np.abs(fft_y) # 取複數的絕對值，即複數的模(雙邊頻譜)
angle_y=np.angle(fft_y) #取複數的角度
normalization_y=abs_y/N #歸一化處理（雙邊頻譜）
normalization_half_y = normalization_y[range(int(N/2))] #由於對稱性，只取一半區間（單邊頻譜）
print(len(fft_y))
xf = fftfreq(N,1/sampling_rate)[:N//2]
ax2.plot(xf,normalization_half_y)
ax2.set_title("FFT")
ax2.set(xlabel='amp', ylabel='Frequency (Hz)')
fig.show()
plt.pause(1000)