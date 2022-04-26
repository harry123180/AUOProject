from matplotlib import pyplot as plt
import  numpy as np
from scipy.fft import fft, fftfreq
file1 = open('all20000.txt', 'r')
Lines = file1.readlines()
ch1 =[]
ch2 = []
ch3 = []
Samping_Rate = 25641
Title = 'Cycle  20'
start_sec = 87.8*0.78
final_sec = start_sec+2
point = int((final_sec-start_sec)*Samping_Rate)

t=  np.linspace(start_sec, final_sec,point)
Hz = np.linspace(0, Samping_Rate,point)
#t=  np.linspace(0, 2,201)
count = 0
# Strips the newline character
k=10
for line in Lines:
    count += 1
    a = line.strip()
    if(count >=start_sec*Samping_Rate and count < final_sec*Samping_Rate):
        ch1.append(float(a.split()[1])*k)
        ch2.append(float(a.split()[2])*k)
        ch3.append(float(a.split()[3])*k)
N=len(ch1)
print(count)
plt.ion()
#y_f = np.abs(np.fft.fft(y_data_OUT))
fig = plt.figure(figsize=(10,8))
ax1 = fig.add_subplot(211)#2個圖 橫版只放1 1號位置
ax2 = fig.add_subplot(212)#2個圖 橫版只放1 2號位置
#print(ch1)
#print(ch2)
ax1.plot(t,ch2)
#plt.plot(t,ch3)
fft_y = fft(ch2)
abs_y = np.abs(fft_y)  # 取複數的絕對值，即複數的模(雙邊頻譜)
angle_y = np.angle(fft_y)  # 取複數的角度
normalization_y = abs_y / N  # 歸一化處理（雙邊頻譜）
normalization_half_y = normalization_y[range(int(N / 2))]  # 由於對稱性，只取一半區間（單邊頻譜）
print(len(fft_y))
xf = fftfreq(N, 1 / Samping_Rate)[:N // 2]
ax2.plot(xf,normalization_half_y)
#plt.legend(['ch1','ch2'])


plt.show()
plt.pause(1000)