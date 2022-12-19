import matplotlib.pyplot as plt
import numpy as np
import random
path = "平均頻譜.txt"
path2="偏移後頻譜.txt"
f = open(path, 'r')
f1=open(path2,'r')
hz = []
amp=[]
temp = []
amp_offset=[]
for i in f.readlines():
    result = i.replace('\n', '').split(" ")
    print(result)
    hz.append(float(result[0]))
    amp.append(float(result[1]))

for i in f1.readlines():
    result = i.replace('\n', '').split(" ")
    amp_offset.append(float(result[1]))
fig,ax=plt.subplots(2,1)
ax[0].set_title("Average spectrum")
ax[0].set_xlabel("Frequency(Hz)")
ax[0].set_ylabel("average amplitude(g)")
ax[0].plot(hz,amp)



ax[0].plot(hz,amp_offset)
plt.show()