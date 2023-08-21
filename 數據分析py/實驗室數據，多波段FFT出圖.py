from matplotlib import pyplot as plt
import numpy as np
from scipy.fft import fft, fftfreq
y_list1=[]
y_list2=[]
y_list3=[]
y_list4=[]
time_list = []

path = 'F:\\AUO_Data\\LM\\SPS10000.txt'
try:
    k=0
    f = open(path, 'r')
    print("opened")
    for i in f.readlines():
        k+=1
        target_t = [69616,121700,172960,223550]

        if (k > target_t[0] and k < target_t[0]+(4096*1)):
            result = i.replace('\n', '').split(" ")
            time_list.append(float(result[0]))  # (float(result[0]))
            y_list1.append(float(result[1]))
        elif(k>target_t[1] and k< target_t[1]+(4096*1)):
            result = i.replace('\n', '').split(" ")
            y_list2.append(float(result[1]))
        elif (k > target_t[2] and k < target_t[2] + (4096 * 1)):
            result = i.replace('\n', '').split(" ")
            y_list3.append(float(result[1]))
        elif (k > target_t[3] and k < target_t[3] + (4096 * 1)):
            result = i.replace('\n', '').split(" ")
            y_list4.append(float(result[1]))
    f.close()
except:
    print("error")
    pass

""" ***********************  """
y_data1 = np.array(y_list1)
y_data2 = np.array(y_list2)
y_data3 = np.array(y_list3)
y_data4 = np.array(y_list4)
time_data = np.array(time_list)
def fft_(data):
    N=len(data)
    Samping_Rate=10200
    fft_y = fft(data)
    abs_y = np.abs(fft_y)  # 取複數的絕對值，即複數的模(雙邊頻譜)
    angle_y = np.angle(fft_y)  # 取複數的角度
    normalization_y = abs_y / N  # 歸一化處理（雙邊頻譜）
    normalization_half_y = normalization_y[range(int(N / 2))]  # 由於對稱性，只取一半區間（單邊頻譜）
    xf = fftfreq(N, 1 / Samping_Rate)[:N // 2]
    #amp0 = normalization_half_y[:-1]
    #amp1 = normalization_half_y[1:]
    #amp = np.array(amp1) - np.array(amp0)
    #amp = np.append(amp,0)
    return xf,normalization_half_y
#y_data3 = np.array(y_list3)
#f.close()
plt.ion()
fig,ax=plt.subplots(2,1)

#ax1 = fig.add_subplot(311)#2個圖 橫版只放1 1號位置
#ax2 = fig.add_subplot(312)#2個圖 橫版只放1 2號位置
#ax3 = fig.add_subplot(313)#2個圖 橫版只放1 2號位置

""" ***********************  """
#ironman_linspace = np.linspace(0,408,len(y_list1)) #建立一個5個值的陣列，在0到1間平均分布

#ironman_linspace2 = np.linspace(0,408,len(y_list2))
label_text = "  Mean Value"
#label_text = "  Standard Deviation Value"
ax[0].plot(time_data,y_data1)
ax[0].set_xlabel("Time(sec)")
ax[0].set_ylabel("Amplitude(g)")
ax[0].set_title("Time")
hz,amp = fft_(y_data1)
total_amp=amp
#ax[1].plot(hz,amp)
hz,amp = fft_(y_data2)
total_amp=np.array(total_amp) + np.array(amp)
#ax[1].plot(hz,amp)
#ax[1].plot(hz,amp)
hz,amp = fft_(y_data4)
total_amp=np.array(total_amp) + np.array(amp)
avg_amp = np.array(total_amp)/3
ax[1].plot(hz,avg_amp)
ax[1].set_xlabel("Frequency(Hz)")
ax[1].set_ylabel("Amplitude(g)")
ax[1].set_title("FFT")
"""
ax[2].plot(ironman_linspace2,y_data3)
ax[2].set_xlabel("Time(Hours)")
ax[2].set_ylabel("Amplitude")
ax[2].set_title("Number3"+label_text)
"""
#存檔結果
f1 = open('偏移後頻譜.txt', 'w')
for i in range(len(avg_amp)):
    f1.write(str(hz[i])+" "+str(amp[i])+'\n')
f1.close()
fig.tight_layout()
fig.show()
plt.pause(100000)