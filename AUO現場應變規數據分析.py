import matplotlib.pyplot as plt

#a = f.read()
#print(len(a))
#b = a.split()
#print(len(b))
path = 'F:\\data3.txt'
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

path = 'F:\\data5.txt'
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

path = 'F:\\data5.txt'
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
path = 'F:\\data6.txt'
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
path = 'F:\\data7.txt'
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

plt.plot(x_axis,strian1)
plt.plot(x_axis,strian2)
plt.grid(True)
plt.xlabel("sec")
plt.ylabel("V")
#plt.ylim(2.7,3)
plt.show()