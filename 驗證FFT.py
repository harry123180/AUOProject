from matplotlib import pyplot as plt
import  numpy as np
from scipy.fft import fft, fftfreq
file1 = open('test_timeDomain.txt', 'r')
freq = open('Freq.txt', 'r')

Lines = file1.readlines()
Lines2 = freq.readlines()
ch1 =[]
ch2 = []
ch3 = []
Title = 'Cycle  20'

t=  np.linspace(0, 2,1024)
Hz = np.linspace(0, 100,1024)
freq_Hz =[]
#t=  np.linspace(0, 2,201)
count = 0
# Strips the newline character
k=1
for line in Lines:
    count += 1
    a = line.strip()
    ch1.append(float(a.split()[0])*k)
for line2 in Lines2:
    a = line2.strip()
    ch2.append(float(a.split()[2])*k)
    freq_Hz.append(float(a.split()[1])*k)
N = 1024
fft_y = fft(ch1)
abs_y=np.abs(fft_y) # 取複數的絕對值，即複數的模(雙邊頻譜)

angle_y=np.angle(fft_y) #取複數的角度

normalization_y=abs_y/N #歸一化處理（雙邊頻譜）

normalization_half_y = normalization_y[range(int(N/2))] #由於對稱性，只取一半區間（單邊頻譜）
print(len(fft_y))

xf = fftfreq(N,1/256)[:N//2]
print(count)
#print(ch1)
#print(ch2)
plt.ion()
#y_f = np.abs(np.fft.fft(ch1))
fig = plt.figure(figsize=(10,8))

ax1 = fig.add_subplot(511)#2個圖 橫版只放1 1號位置
ax2 = fig.add_subplot(512)#2個圖 橫版只放1 2號位置
ax3 = fig.add_subplot(513)#2個圖 橫版只放1 2號位置
ax4 = fig.add_subplot(514)#2個圖 橫版只放1 2號位置
ax5 = fig.add_subplot(515)#2個圖 橫版只放1 2號位置
ax1.plot(t,ch1)
ax1.set_title(Title)
ax1.set(xlabel='Time(Sec)', ylabel='Acceleration(g)')
#ax2.plot(t,ch2)
mix = []

y_f = np.fft.fft(ch1,axis = 0)
x_f = np.fft.fftfreq(N,1.0/256)
print(max(x_f),min(x_f))
for jj in range(len(y_f)):
    mix.append(pow(pow(y_f.real[jj],2)+pow(y_f.imag[jj],2),0.5))
ax2.plot(Hz,y_f.real,Hz,y_f.imag)
ax3.plot(freq_Hz,ch2)
ax4.plot(xf, normalization_half_y)
ax5.plot(x_f,mix)
#plt.xscale("log")
#plt.axis('off')
fig.show()
plt.pause(1000)