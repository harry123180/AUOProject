from matplotlib import pyplot as plt
import  numpy as np
from scipy.fft import fft, fftfreq
file1 = open('all20000.txt', 'r')
Lines = file1.readlines()
ch1 =[]
ch2 = []
ch3 = []
Title = 'static stack dynamic'
Samping_Rate = 25641# 10k = 10204 20k = 25641
############10K Hz################
start_sec =[4.16,10] #第一段 1~5
final_sec =[6.16,12] #
#start_sec = [189.6,226,263.5,300.3,338.3]#第二段 6~10
#final_sec = [191.6,228,265.5,302.3,340.3]
#start_sec = [374.8,410.77,443.3,477.1,509.11]#第三段11~15
#final_sec = [376.8,412.77,445.3,479.1,511.11]
#start_sec =[544.15,581.0,619.88,654.5,689.7]#第四段16~20
#final_sec =[546.15,583.0,621.88,656.5,691.7]
#################20k Hz####################
#start_sec = [4.6,26.9,58.8,87.8,116.8]

#start_sec = [145.9,181,210.3,240.6,270]

#start_sec = [298.9,328,357.6,386.7,415.7]

#start_sec = [444.5,473.5,508.2,537.2,566.4]


for s_ in range(len(start_sec)):
    start_sec[s_] = start_sec[s_]*0.98
final_sec = [start_sec[0]+2,start_sec[1]+2]
#################################################
point = int((final_sec[0]-start_sec[0])*Samping_Rate)
t=  np.linspace(start_sec[0], final_sec[0],1024)
count = 0
data_2d_list =[[],[]]
k=1
for line in Lines:
    count += 1
    a = line.strip()
    for j in range(len(start_sec)):
        if(count >=start_sec[j]*Samping_Rate and count < final_sec[j]*Samping_Rate):
            if(count%1 ==0):
                data_2d_list[j].append(float(a.split()[2])*k-0.001)
                #ch2.append(float(a.split()[2])*k)
                #ch3.append(float(a.split()[3])*k)


print(count)
#print(ch1)
#print(ch2)
N=len(data_2d_list[0])

#data_2d_list[1] = [x -0.0045 for x in data_2d_list[1]]
print(len(data_2d_list[0]))
color_list = ['orange','blue']
for ss in range(2):
    print(ss)
    fft_y = fft(data_2d_list[ss])
    abs_y = np.abs(fft_y)  # 取複數的絕對值，即複數的模(雙邊頻譜)
    angle_y = np.angle(fft_y)  # 取複數的角度
    normalization_y = abs_y / N  # 歸一化處理（雙邊頻譜）
    normalization_half_y = normalization_y[range(int(N / 2))]  # 由於對稱性，只取一半區間（單邊頻譜）
    print(len(fft_y))
    xf = fftfreq(N, 1 / Samping_Rate)[:N // 2]
    if(ss ==1):
        normalization_half_y = [x * 100 for x in normalization_half_y]
        normalization_half_y[0] = 0
    plt.plot(xf ,normalization_half_y, alpha = 0.9,color = color_list[ss])
#plt.plot(Hz,np.abs(np.fft.fft(data_2d_list[1])))
plt.title('static stack dynamic')
plt.xlabel('Frequency (Hz)')
plt.ylabel('Amplitude')
plt.legend(['dynamic','static x100'])
#plt.legend(['cycle6','cycle7','cycle8','cycle9','cycle10'])
#plt.legend(['cycle11','cycle12','cycle13','cycle14','cycle15'])
#plt.legend(['cycle16','cycle17','cycle18','cycle19','cycle20'])
#plt.xscale("log")
#y_f = np.abs(np.fft.fft(ch1))

plt.show()
plt.pause(1000)