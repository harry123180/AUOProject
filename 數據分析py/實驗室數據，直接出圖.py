from matplotlib import pyplot as plt
import numpy as np
y_list1=[]
y_list2=[]
y_list3=[]
time_list = []

def Mean(array_org):
    total = 0
    for i in range(len(array_org)):
        total += array_org[i]
    return total/len(array_org)

path = 'I:\\AUO_Data\\LM\\SPS10000.txt'

try:
    Mean1 = []
    Mean2 = []
    Mean3 = []
    k=0
    print("open")
    f = open(path, 'r')
    print("opened")
    for i in f.readlines():
        k+=1
        result = i.replace('\n', '').split(" ")
        print(result)
        time_list.append(k)#(float(result[0]))
        y_list1.append(float(result[1]))
        y_list2.append(float(result[2]))
        #y_list3.append(float(result[3]))
        #print(y_list1)
    #y_list1.append(Mean(Mean1))
    #y_list2.append(Mean(Mean2))
    #y_list3.append(Mean(Mean3))
    f.close()
except:
    print("error")
    pass

""" ***********************  """
y_data1 = np.array(y_list1)
y_data2 = np.array(y_list2)
time_data = np.array(time_list)
#y_data3 = np.array(y_list3)
f.close()
plt.ion()
fig,ax=plt.subplots(2,1)

#ax1 = fig.add_subplot(311)#2個圖 橫版只放1 1號位置
#ax2 = fig.add_subplot(312)#2個圖 橫版只放1 2號位置
#ax3 = fig.add_subplot(313)#2個圖 橫版只放1 2號位置

""" ***********************  """
#ironman_linspace = np.linspace(0,408,len(y_list1)) #建立一個5個值的陣列，在0到1間平均分布

#ironman_linspace2 = np.linspace(0,408,len(y_list2))
label_text = "  Mean Value"
#label_text = "  Standard Deviation Value"
ax[0].plot(time_data,y_data1)
ax[0].set_xlabel("Time(ms)")
ax[0].set_ylabel("Amplitude")
ax[0].set_title("Number1"+label_text)
ax[1].plot(time_data,y_data2)
ax[1].set_xlabel("Time(ms)")
ax[1].set_ylabel("Amplitude")
ax[1].set_title("Number2"+label_text)

"""
ax[2].plot(ironman_linspace2,y_data3)
ax[2].set_xlabel("Time(Hours)")
ax[2].set_ylabel("Amplitude")
ax[2].set_title("Number3"+label_text)
"""

fig.tight_layout()
fig.show()
plt.pause(100000)