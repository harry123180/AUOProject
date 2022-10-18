from matplotlib import pyplot as plt
import numpy as np
y_list1=[]
y_list2=[]
y_list3=[]
def Mean(array_org):
    total = 0
    for i in range(len(array_org)):
        total += array_org[i]
    return total/len(array_org)
total_hours=0
for j in range(81):
    path = 'G:\\AUOdata\\output'+str(j)+'.txt'
    try:
        Mean1 = []
        Mean2 = []
        Mean3 = []
        k=1
        f = open(path, 'r')
        for i in f.readlines():
            result = i.split(" ")
            if(int(result[0])==3):
                #print(result[0])
                y_list1.append(float(result[k]))
                #Mean1.append(float(result[k]))

            if (int(result[0]) == 1):
                y_list2.append(float(result[k+1]))
                y_list3.append(float(result[k+2]))
                #Mean2.append(float(result[k+1]))
                #Mean3.append(float(result[k+2]))
        #y_list1.append(Mean(Mean1))
        #y_list2.append(Mean(Mean2))
        #y_list3.append(Mean(Mean3))
        f.close()
        total_hours+=1
    except:
        pass

""" ***********************  """
y_data1 = np.array(y_list1)
y_data2 = np.array(y_list2)
y_data3 = np.array(y_list3)
f.close()
plt.ion()
fig,ax=plt.subplots(3,1)

#ax1 = fig.add_subplot(311)#2個圖 橫版只放1 1號位置
#ax2 = fig.add_subplot(312)#2個圖 橫版只放1 2號位置
#ax3 = fig.add_subplot(313)#2個圖 橫版只放1 2號位置

""" ***********************  """
ironman_linspace = np.linspace(0,408,len(y_list1)) #建立一個5個值的陣列，在0到1間平均分布

ironman_linspace2 = np.linspace(0,408,len(y_list2))
label_text = "  Mean Value"
#label_text = "  Standard Deviation Value"
ax[0].plot(ironman_linspace,y_data1)
ax[0].set_xlabel("Time(Hours)")
ax[0].set_ylabel("Amplitude")
ax[0].set_title("Number1"+label_text)
ax[1].plot(ironman_linspace2,y_data2)
ax[1].set_xlabel("Time(Hours)")
ax[1].set_ylabel("Amplitude")
ax[1].set_title("Number2"+label_text)
ax[2].plot(ironman_linspace2,y_data3)
ax[2].set_xlabel("Time(Hours)")
ax[2].set_ylabel("Amplitude")
ax[2].set_title("Number3"+label_text)

fig.tight_layout()
fig.show()
plt.pause(100000)