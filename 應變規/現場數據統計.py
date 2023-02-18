import matplotlib.pyplot as plt
"""
這個程式讀取原始以小時為單位，進行統計五天的資料並繪圖，數據放在同一個根目錄，有把雜訊濾除

"""
#a = f.read()
#print(len(a))
#b = a.split()
#print(len(b))
path = 'data3.txt'
f = open(path, 'r')
lines = f.readlines()
strian1=[]
strian2 = []
counter = 0
x_axis = []
for line in lines :
    string  = line.replace('\n', '')
    value_list = string.split(" ")
    strian1.append(float(value_list[0])/10000)
    strian2.append((float(value_list[1]))/10000)
    x_axis.append(counter)
    counter+=8
f.close()

path = 'data5.txt'
f = open(path, 'r')
lines = f.readlines()
for line in lines :
    string  = line.replace('\n', '')
    value_list = string.split(" ")
    strian1.append(float(value_list[0])/10000)
    strian2.append((float(value_list[1]))/10000)
    x_axis.append(counter)
    counter+=8
f.close()

path = 'data5.txt'
f = open(path, 'r')
lines = f.readlines()
for line in lines :
    string  = line.replace('\n', '')
    value_list = string.split(" ")
    strian1.append(float(value_list[0])/10000)
    strian2.append((float(value_list[1]))/10000)
    x_axis.append(counter)
    counter+=8
f.close()
path = 'data6.txt'
f = open(path, 'r')
lines = f.readlines()
for line in lines :
    string  = line.replace('\n', '')
    value_list = string.split(" ")
    strian1.append(float(value_list[0])/10000)
    strian2.append((float(value_list[1]))/10000)
    x_axis.append(counter)
    counter+=8
f.close()
path = 'data7.txt'
f = open(path, 'r')
lines = f.readlines()
for line in lines :
    string  = line.replace('\n', '')
    value_list = string.split(" ")
    strian1.append(float(value_list[0])/10000)
    strian2.append((float(value_list[1]))/10000)
    x_axis.append(counter)
    counter+=8
f.close()
path = 'F:\\data8.txt'
f = open(path, 'r')
lines = f.readlines()

for line in lines :
    string  = line.replace('\n', '')
    value_list = string.split(" ")
    strian1.append(float(value_list[0])/10000)
    strian2.append((float(value_list[1]))/10000)
    x_axis.append(counter)
    counter+=8
f.close()
def replace_noise_with_previous_value(lst):
    threshold =0.12
    for i in range(1, len(lst)):
        if abs(lst[i] - lst[i-1]) > threshold:
            lst[i] = lst[i-1]
    return lst
import numpy as np
# 每 540 个元素进行统计，计算每个子列表的平均值和标准差
strian1=replace_noise_with_previous_value(strian1)
strian2=replace_noise_with_previous_value(strian2)
grouped_data = np.array(strian1).reshape(-1, 540)
grouped_data2 = np.array(strian2).reshape(-1, 540)
# 计算每组数据的平均值和标准差
means = np.mean(grouped_data, axis=1)
stds = np.std(grouped_data, axis=1)
means2 = np.mean(grouped_data2, axis=1)
stds2 = np.std(grouped_data2, axis=1)


# 生成 x 轴的数值
x = np.arange(1, 121)
print(stds.shape,x.shape)
#plt.plot(x_axis,strian1)
#plt.plot(x_axis,strian2)
fig, ax = plt.subplots()
ax.errorbar(x, means, yerr=stds, fmt='-o', capsize=3)
ax.errorbar(x, means2, yerr=stds2, fmt='-o', capsize=3)
ax.set_xlabel('Hour')
ax.set_ylabel('V')
ax.set_title('Strain gauge data')
#plt.grid(True)
#plt.xlabel("sec")
#plt.ylabel("V")
#plt.ylim(2.7,3)
plt.show()