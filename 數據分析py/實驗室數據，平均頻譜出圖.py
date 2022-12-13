import matplotlib.pyplot as plt
import numpy as np

path = "平均頻譜.txt"
f = open(path, 'r')
hz = []
amp=[]
for i in f.readlines():
    result = i.replace('\n', '').split(" ")
    print(result)
    hz.append(float(result[0]))
    amp.append(float(result[1]))
plt.title("Average spectrum")
plt.xlabel("Frequency(Hz)")
plt.ylabel("average amplitude(g)")
plt.plot(hz,amp)
plt.show()