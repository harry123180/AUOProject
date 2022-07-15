from matplotlib import pyplot as plt
import  numpy as np

# 壓電式加速規量測值
def Mean(TimeArray):
    Total = 0
    for i in range(len(TimeArray)):
        Total += TimeArray[i]
    return Total/len(TimeArray)

file1 = open('MEMS_MCU_Data.txt', 'r')
Lines = file1.readlines()
ch1 =[]
buffer =[0.0]*1024
結果=[]
Title = 'Cycle  20'


#t=  np.linspace(0, 2,201)
count = 0
# Strips the newline character
rs = []
e = 0
for line in Lines:


    a = line.strip()
    #print(len(a.split()),a.split()[2])
    ch1.append(float(a.split()[2])-1.1)
    buffer[count] = float(a.split()[2])
    e+=float(a.split()[2])-1.1
    count += 1
print(e/len(ch1))
t=  np.linspace(0, len(ch1),len(ch1))
#Hz = np.linspace(0, 10000,point)

plt.ion()
fig = plt.figure(figsize=(10,8))
ax1 = fig.add_subplot(111)#2個圖 橫版只放1 1號位置
ax1.plot(t,ch1)
ax1.set_title(Title)
ax1.set(xlabel='Time(Sec)', ylabel='Acceleration(g)')
y_f = np.abs(np.fft.fft(ch1))
fig.show()
plt.pause(1000)
# 存成txt