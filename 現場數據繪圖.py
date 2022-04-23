from matplotlib import pyplot as plt
import  numpy as np
file1 = open('all10000.txt', 'r')
Lines = file1.readlines()
ch1 =[]
ch2 = []
ch3 = []
Title = 'Cycle  20'
start_sec = 678
final_sec = 749
point = (final_sec-start_sec)*10000
t=  np.linspace(start_sec, final_sec,point)
Hz = np.linspace(0, 10000,point)
#t=  np.linspace(0, 2,201)
count = 0
# Strips the newline character
k=1
for line in Lines:
    count += 1
    a = line.strip()

    if(count >=start_sec*10000 and count < final_sec*10000):
        if(count%1 ==0):
            ch1.append(float(a.split()[1])*k)
            ch2.append(float(a.split()[2])*k)
            ch3.append(float(a.split()[3])*k)

    if(count > 20000000000):
        break
print(count)
#print(ch1)
#print(ch2)
plt.ion()
#y_f = np.abs(np.fft.fft(y_data_OUT))
fig = plt.figure(figsize=(10,8))
ax1 = fig.add_subplot(111)#2個圖 橫版只放1 1號位置
#ax2 = fig.add_subplot(312)#2個圖 橫版只放1 2號位置
#ax3 = fig.add_subplot(212)#2個圖 橫版只放1 2號位置
ax1.plot(t,ch1)
ax1.set_title(Title)
ax1.set(xlabel='Time(Sec)', ylabel='Acceleration(g)')
#ax2.plot(t,ch2)

y_f = np.abs(np.fft.fft(ch1))
#ax3.plot(Hz,y_f)
#plt.xscale("log")
#plt.axis('off')
fig.show()
plt.pause(1000)