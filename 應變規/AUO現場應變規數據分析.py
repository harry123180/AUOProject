import matplotlib.pyplot as plt
"""
這個程式讀取原始五天的資料並繪圖，數據放在同一個根目錄

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
        #print(abs(lst[i] - lst[i-1]) )
        if abs(lst[i] - lst[i-1]) > threshold:
            print("成立")
            lst[i] = lst[i-1]
    return lst
strian1=replace_noise_with_previous_value(strian1)
strian2=replace_noise_with_previous_value(strian2)
plt.plot(x_axis,strian1)
plt.plot(x_axis,strian2)
plt.grid(True)
plt.xlabel("sec")
plt.ylabel("V")
#plt.ylim(2.7,3)
plt.show()