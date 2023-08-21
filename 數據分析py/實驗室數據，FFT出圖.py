from matplotlib import pyplot as plt
import numpy as np
from scipy.fft import fft, fftfreq
y_list1=[]
y_list2=[]
y_list3=[]
time_list = []
def Mean(array_org):
    total = 0
    for i in range(len(array_org)):
        total += array_org[i]
    return total/len(array_org)

path = 'F:\\AUO_Data\\LM\\SPS10000.txt'
try:
    Mean1 = []
    Mean2 = []
    Mean3 = []
    k=0
    print("open")
    f = open(path, 'r')
    print("opened")
    for i in f.readlines():
        k+=1
        target_t = 1149340
        if (k > target_t and k < target_t+(4096*1)):
            result = i.replace('\n', '').split(" ")
            time_list.append(float(result[0]))  # (float(result[0]))
            print(result)
            y_list1.append(float(result[1]))
            y_list2.append(float(result[2]))
        #y_list3.append(float(result[3]))
        #print(y_list1)
    #y_list1.append(Mean(Mean1))
    #y_list2.append(Mean(Mean2))
    #y_list3.append(Mean(Mean3))
    f.close()
except:
    print("error")
    pass

""" ***********************  """
y_data1 = np.array(y_list1)
y_data2 = np.array(y_list2)
time_data = np.array(time_list)
N=len(y_data1)
Samping_Rate=10200
fft_y = fft(y_data1)
abs_y = np.abs(fft_y)  # 取複數的絕對值，即複數的模(雙邊頻譜)
angle_y = np.angle(fft_y)  # 取複數的角度
normalization_y = abs_y / N  # 歸一化處理（雙邊頻譜）
normalization_half_y = normalization_y[range(int(N / 2))]  # 由於對稱性，只取一半區間（單邊頻譜）
#print(len(fft_y))
xf = fftfreq(N, 1 / Samping_Rate)[:N // 2]
#y_data3 = np.array(y_list3)
f.close()
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
ax[1].plot(xf,normalization_half_y)
ax[1].set_xlabel("Frequency(Hz)")
ax[1].set_ylabel("Amplitude(g)")
ax[1].set_title("FFT")
"""
ax[2].plot(ironman_linspace2,y_data3)
ax[2].set_xlabel("Time(Hours)")
ax[2].set_ylabel("Amplitude")
ax[2].set_title("Number3"+label_text)
"""

fig.tight_layout()
fig.show()
plt.pause(100000)