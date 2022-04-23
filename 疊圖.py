from matplotlib import pyplot as plt
import  numpy as np
file1 = open('all10000.txt', 'r')
Lines = file1.readlines()
ch1 =[]
ch2 = []
ch3 = []
Title = 'Cycle  20'
Samping_Rate = 10000#採樣頻率
start_sec = [51.6,90.4]
final_sec = [53.6,92.4]
point = int((final_sec[0]-start_sec[0])*Samping_Rate)
t=  np.linspace(start_sec[0], final_sec[0],point)
Hz = np.linspace(0, Samping_Rate,point)
#t=  np.linspace(0, 2,201)
count = 0
data_2d_list =[[],[]]
k=1
for line in Lines:
    count += 1
    a = line.strip()
    for j in range(len(start_sec)):
        if(count >=start_sec[j]*Samping_Rate and count < final_sec[j]*Samping_Rate):
            if(count%1 ==0):
                data_2d_list[j].append(float(a.split()[1])*k)
                #ch2.append(float(a.split()[2])*k)
                #ch3.append(float(a.split()[3])*k)

    if(count > 20000000000):
        break
print(count)
#print(ch1)
#print(ch2)
plt.plot(t,data_2d_list[0])
plt.plot(t,data_2d_list[1])

plt.legend(['ch1','ch2'])
#y_f = np.abs(np.fft.fft(ch1))

plt.show()
plt.pause(1000)