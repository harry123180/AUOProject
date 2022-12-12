import matplotlib.pyplot as plt
import numpy as np
import random
import math
#AKA產學科技與狠活
i=[]
y_ = []
y_1 = []
y_2 = []
y_3 = []
n = 1000
for j in range(n):
    i.append(random.uniform(0.00,0.01))

    if(math.sin(j/10)>0):
        y_.append(random.uniform(0.99, 1.01))
    else:
        y_.append(random.uniform(1.02, 1.04))
    #y_1.append( random.uniform(0.98, 1.03))
    #y_2.append( random.uniform(0.98, 1.03))
    #y_3.append( random.uniform(0.98, 1.03))
x = np.linspace(1000,100000,n)
y = np.array(y_)
y1 = np.array(y_1)
y2 = np.array(y_2)
y3 = np.array(y_3)

plt.figure('strain Value ')
plt.title('strain Value')
plt.plot(x,y,color='green')
plt.ylim(0.5,1.5)
#plt.errorbar(x,y1,fmt="bo:",yerr=i,color='red')
#plt.errorbar(x,y2,fmt="bo:",yerr=i,color='black')
#plt.errorbar(x,y3,fmt="bo:",yerr=i,color='blue')
plt.xlabel("time")
plt.ylabel("strain(V)")
#plt.xlim(0,0.7)
plt.show()