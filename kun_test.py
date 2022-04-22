import numpy as np
import h5py
from scipy import signal
from matplotlib import pyplot as plt
def ROI_list(Target_array, min, max):
    min_indx = [i for i in range(0, min)]
    modifiedArray = np.delete(Target_array, min_indx,None)
    max = max - min
    min_indx = [i for i in range(max,len(modifiedArray))]
    return np.delete(modifiedArray, min_indx, None)
plt.ion()
fig = plt.figure(figsize=(10,8))
ax1 = fig.add_subplot(211)#2個圖 橫版只放1 1號位置
ax2 = fig.add_subplot(212)#2個圖 橫版只放1 2號位置
final_fft  = np.linspace(0, 0,84316)
for i in range(100,163):
    if ( i!= 152):
        file_name ='exp1_'+str(i)
        f = h5py.File('G:\AUOProject\\' + file_name+  '.mat','r')

        var = f.items()
        print(var)
        for v in var:
            print(v)

        data = f.get(file_name+'/Y/Data')
        time_data = f.get(file_name+'/X/Data')
        obj_Y_OUT = f[data[1][0]]#輸出

        obj_Y_IN = f[data[0][0]]#輸入
        obj_X = f[time_data[0][0]]
        start_point = 15684
        y_data_OUT = ROI_list(np.array(obj_Y_OUT),start_point,len(np.array(obj_Y_OUT))-1)
        y_data_IN = ROI_list(np.array(obj_Y_IN),start_point,len(np.array(obj_Y_IN))-1)

        #print(y_data_IN)
        x_data = ROI_list(np.array(obj_X),15684,len(np.array(obj_X))-1)
        #print(len(x_data),len(y_data_OUT))
        #創建畫布

        #ax1.plot(x_data,y_data_OUT)
        #ax1.plot(x_data,y_data_IN)
        #fftData=np.fft.rfft(y_data_OUT) #fft amplitude axis
        #fftTime=np.fft.rfftfreq(100001,1.)#fft freq axis
        print(y_data_OUT)
        y_f = np.abs(np.fft.fft(y_data_OUT))
        y_f2 = np.abs(np.fft.fft(y_data_IN))
        x_f = np.linspace(0, 10000,84316)
        indx_yf = y_f.tolist().index(max(y_f.tolist()))

        final_fft[indx_yf] = max(y_f.tolist())
        print(len(x_f))

        #ax2.plot(x_f,y_f2)
ax2.plot(x_f,final_fft)
plt.xscale("log")
fig.show()
plt.pause(100)
#data = np.array(data) # For converting to a NumPy array
#print(data)