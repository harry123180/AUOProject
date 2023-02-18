import matplotlib.pyplot as plt
"""
這個程式讀取原始五天的資料並繪圖，數據放在同一個根目錄

"""

x_axis = []

path = ['011.txt','013.txt','014.txt']
def load_data(path_name_list):
    x = 0
    strian = []
    counter = 0
    for u in range(len(path_name_list)):
        f = open(path_name_list[u], 'r')
        lines = f.readlines()
        for line in lines :
            string  = line.replace('\n', '')
            value_list = string.split("\t")
            strian.append(float(value_list[1]))
            counter+=1
            if(counter==1614):
                counter=0
                x+=1
        f.close()
    return strian,x,counter
strian1,x,counter = load_data(path)
print(x,counter,len(strian1))
def remove_after_n(lst, n):
    return lst[:n+1]
def remove_elements(array, n):
    return array[:n]
strian1 = remove_after_n(strian1,x*1614-1)
print(x,counter,len(strian1))
import numpy as np
grouped_data = np.array(strian1).reshape(-1, 1614)
means = np.mean(grouped_data, axis=1)
stds = np.std(grouped_data, axis=1)



means= means.tolist()
print(int(x/60))
a = remove_after_n(means,int(x/60)*60-1)
grouped_data2 = np.array(a).reshape(-1, 60)
means2 = np.mean(grouped_data2, axis=1)
stds2 = np.std(grouped_data2, axis=1)
print(grouped_data2.shape)
fig, ax = plt.subplots()

x = np.arange(1, int(x/60)+1)
#ax.plot(x,means2)
ax.errorbar(x, means2, yerr=stds2, fmt='-o', capsize=1)
ax.set_xlabel('Hour')
ax.set_ylabel('V')
ax.set_title('Strain gauge data')

plt.show()