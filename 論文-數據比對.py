from matplotlib import pyplot as plt
import  numpy as np
# 壓電式加速規量測值
def Mean(TimeArray):
    Total = 0
    for i in range(len(TimeArray)):
        Total += TimeArray[i]
    return Total/len(TimeArray)

file1 = open('0.txt', 'r')
Lines = file1.readlines()
ch1 =[]
buffer =[0.0]*1024
結果=[]
Title = 'Cycle  20'


#t=  np.linspace(0, 2,201)
count = 0
# Strips the newline character
rs = []
for line in Lines:


    a = line.strip()
    ch1.append(float(a.split()[1]))
    buffer[count] = float(a.split()[1])
    count += 1
    if (count % 1023 ==0):
        rs.append(Mean(buffer))
        count = 0
print(rs)
t=  np.linspace(0, len(rs),len(rs))
#Hz = np.linspace(0, 10000,point)

plt.ion()
fig = plt.figure(figsize=(10,8))
ax1 = fig.add_subplot(111)#2個圖 橫版只放1 1號位置
ax1.plot(t,rs)
ax1.set_title(Title)
ax1.set(xlabel='Time(Sec)', ylabel='Acceleration(g)')
y_f = np.abs(np.fft.fft(ch1))
fig.show()
plt.pause(1000)
# 存成txt