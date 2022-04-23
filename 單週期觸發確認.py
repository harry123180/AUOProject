from matplotlib import pyplot as plt
import  numpy as np
file1 = open('all10000.txt', 'r')
Lines = file1.readlines()
ch1 =[]
ch2 = []
ch3 = []
Samping_Rate = 20000
Title = 'Cycle  20'
start_sec = 689.7
final_sec = start_sec+2
point = int((final_sec-start_sec)*Samping_Rate)

t=  np.linspace(start_sec, final_sec,point)
Hz = np.linspace(0, Samping_Rate,point)
#t=  np.linspace(0, 2,201)
count = 0
# Strips the newline character
k=1
for line in Lines:
    count += 1
    a = line.strip()
    if(count >=start_sec*Samping_Rate and count < final_sec*Samping_Rate):
        ch1.append(float(a.split()[1])*k)
        ch2.append(float(a.split()[2])*k)
        ch3.append(float(a.split()[3])*k)

print(count)
#print(ch1)
#print(ch2)
plt.plot(t,ch1)
#plt.plot(t,ch3)

#plt.legend(['ch1','ch2'])
y_f = np.abs(np.fft.fft(ch1))

plt.show()
plt.pause(1000)