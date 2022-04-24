from matplotlib import pyplot as plt
import  numpy as np
file1 = open('all20000.txt', 'r')
Lines = file1.readlines()
ch1 =[]
ch2 = []
ch3 = []
Title = 'Cycle  20'
Samping_Rate = 20000
############10K Hz################
#start_sec =[4.16,51.6,90.4,125.3,160.8] #第一段 1~5
#final_sec =[6.16,53.6,92.4,127.3,162.8] #
#start_sec = [189.6,226,263.5,300.3,338.3]#第二段 6~10
#final_sec = [191.6,228,265.5,302.3,340.3]
#start_sec = [374.8,410.77,443.3,477.1,509.11]#第三段11~15
#final_sec = [376.8,412.77,445.3,479.1,511.11]
#start_sec =[544.15,581.0,619.88,654.5,689.7]#第四段16~20
#final_sec =[546.15,583.0,621.88,656.5,691.7]
#################20k Hz####################
#start_sec = [4.6,26.9,58.8,87.8,116.8]
#final_sec = [start_sec[0]+2,start_sec[1]+2,start_sec[2]+2,start_sec[3]+2,start_sec[4]+2]
#start_sec = [145.9,181,210.3,240.6,270]
#final_sec = [start_sec[0]+2,start_sec[1]+2,start_sec[2]+2,start_sec[3]+2,start_sec[4]+2]
#start_sec = [298.9,328,357.6,386.7,415.7]
#final_sec = [start_sec[0]+2,start_sec[1]+2,start_sec[2]+2,start_sec[3]+2,start_sec[4]+2]
start_sec = [444.5,473.5,508.2,537.2,566.4]
final_sec = [start_sec[0]+2,start_sec[1]+2,start_sec[2]+2,start_sec[3]+2,start_sec[4]+2]


#################################################
point = int((final_sec[0]-start_sec[0])*Samping_Rate)
t=  np.linspace(start_sec[0], final_sec[0],1024)
Hz = np.fft.rfftfreq(1024,1./Samping_Rate)#fft freq axis
#t=  np.linspace(0, 2,201)
count = 0
data_2d_list =[[],[],[],[],[]]
k=1
for line in Lines:
    count += 1
    a = line.strip()
    for j in range(len(start_sec)):
        if(count >=start_sec[j]*Samping_Rate+2048 and count < start_sec[j]*Samping_Rate+2048+1024):
            if(count%1 ==0):
                data_2d_list[j].append(float(a.split()[1])*k)
                #ch2.append(float(a.split()[2])*k)
                #ch3.append(float(a.split()[3])*k)


print(count)
#print(ch1)
#print(ch2)
print(len(data_2d_list[1][1024:2048]))
for ss in range(5):
    plt.plot(Hz,np.abs(np.fft.rfft(data_2d_list[ss])))
#plt.plot(Hz,np.abs(np.fft.fft(data_2d_list[1])))

plt.legend(['cycle16','cycle17','cycle18','cycle19','cycle20'])
#plt.xscale("log")
#y_f = np.abs(np.fft.fft(ch1))

plt.show()
plt.pause(1000)