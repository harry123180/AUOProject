from matplotlib import pyplot as plt
import  numpy as np
file1 = open('0.txt', 'r')
Lines = file1.readlines()
ch1 =[]
buffer =[0]*1024
結果=[]
Title = 'Cycle  20'


#t=  np.linspace(0, 2,201)
count = 0
# Strips the newline character
k=1
for line in Lines:
    count += 1
    a = line.strip()
    ch1.append(float(a.split()[1])*k)
print(count)
t=  np.linspace(0, count,count)
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