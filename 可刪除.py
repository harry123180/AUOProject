
import math

import matplotlib.pyplot as plt
g_of_t = []
freq = 1
time_axis = []
samlping_time = 10
sampling_rate = 10
for i in range(sampling_rate*samlping_time):
    time_axis.append(((i/sampling_rate))/samlping_time)
    if(i != 0):
        g_of_t.append(math.sin(freq*(i/0.628)))
    else:
        g_of_t.append(math.sin(freq*0))


#print(g_of_t)
freq_axis = []
amp_axis = []
for f in range(0,int(freq*200),1):
    f_ = f/100
    real = 0
    im = 0
    for t_k in range(0,len(g_of_t)):
        real = real + g_of_t[t_k]*math.cos(-2*math.pi*f_*t_k)
        im = im +g_of_t[t_k]*math.sin(-2*math.pi*f_*t_k)
    real = real/len(g_of_t)
    im = im/len(g_of_t)
    total = pow(pow(real,2)+pow(im,2),0.5)
    freq_axis.append(f_)
    amp_axis.append(total)
    print(f_,total)
plt.figure()
plt.plot(time_axis, g_of_t)
plt.xlabel('time')
plt.ylabel('g_of_t')
plt.figure()
plt.plot(freq_axis, amp_axis)
plt.xlabel('Hz')
plt.ylabel('amp')
plt.show()